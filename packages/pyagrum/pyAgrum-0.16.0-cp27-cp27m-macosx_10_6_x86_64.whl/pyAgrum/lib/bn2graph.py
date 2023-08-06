#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) Copyright by Pierre-Henri Wuillemin, UPMC, 2017
# (pierre-henri.wuillemin@lip6.fr)

# Permission to use, copy, modify, and distribute this
# software and its documentation for any purpose and
# without fee or royalty is hereby granted, provided
# that the above copyright notice appear in all copies
# and that both that copyright notice and this permission
# notice appear in supporting documentation or portions
# thereof, including modifications, that you make.

# THE AUTHOR P.H. WUILLEMIN  DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER
# RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE
# OR PERFORMANCE OF THIS SOFTWARE!

from __future__ import print_function

import time
import math
import hashlib

import matplotlib.pyplot as plt
import numpy as np
import pyAgrum as gum
import pydotplus as dot
import shutil

__GRAPHBLACK = "#4A4A4A"


def forDarkTheme():
  """ change the color for arcs and text in graphs to be more visible in dark theme
  """
  global __GRAPHBLACK
  __GRAPHBLACK = "#AAAAAA"


def forLightTheme():
  """ change the color for arcs and text in graphs to be more visible in light theme
  """
  global __GRAPHBLACK
  __GRAPHBLACK = "#202020"


def getBlackInTheme():
  """ return the color used for arc and text in graphs
  """
  global __GRAPHBLACK
  return __GRAPHBLACK


def _proba2rgb(p, cmap, withSpecialColor):
  (r, g, b, _) = cmap(p)
  r = "%02x" % int(r * 256)
  g = "%02x" % int(g * 256)
  b = "%02x" % int(b * 256)

  if withSpecialColor:  # add special color for p=0 or p=1
    if p == 0.0:
      r, g, b = "FF", "33", "33"
    elif p == 1.0:
      r, g, b = "AA", "FF", "FF"

  return r, g, b


def _proba2color(p, cmap):
  r, g, b = _proba2rgb(p, cmap, withSpecialColor=False)
  return "#" + r + g + b


def _proba2bgcolor(p, cmap):
  r, g, b = _proba2rgb(p, cmap, withSpecialColor=True)
  return "#" + r + g + b


def _proba2fgcolor(p, cmap):
  if max([eval("0x" + s[0]) for s in _proba2rgb(p, cmap, withSpecialColor=True)]) <= 12:
    return "#FFFFFF"
  else:
    return "#000000"


def BN2dot(bn, size="4", nodeColor=None, arcWidth=None, arcColor=None, cmapNode=None, cmapArc=None, showMsg=None):
  """
  create a pydotplus representation of the BN

  :param pyAgrum.BayesNet bn:
  :param string size: size of the rendered graph
  :param nodeColor: a nodeMap of values (between 0 and 1) to be shown as color of nodes (with special colors for 0 and 1)
  :param arcWidth: a arcMap of values to be shown as width of arcs
  :param arcColor: a arcMap of values (between 0 and 1) to be shown as color of arcs
  :param cmapNode: color map to show the vals of Nodes
  :param cmapArc: color map to show the vals of Arcs.
  :param showMsg: a nodeMap of values to be shown as tooltip

  :return: the desired representation of the BN as a dot graph
  """
  if cmapNode is None:
    cmapNode = plt.get_cmap('summer')

  if cmapArc is None:
    cmapArc = plt.get_cmap('BuGn')

  if arcWidth is not None:
    minarcs = min(arcWidth.values())
    maxarcs = max(arcWidth.values())

  graph = dot.Dot(graph_type='digraph', bgcolor="transparent")

  for n in bn.names():
    if nodeColor is None or n not in nodeColor:
      bgcol = "#404040"
      fgcol = "#FFFFFF"
      res = ""
    else:
      bgcol = _proba2bgcolor(nodeColor[n], cmapNode)
      fgcol = _proba2fgcolor(nodeColor[n], cmapNode)
      res = " : {0:2.5f}".format(nodeColor[n] if showMsg is None else showMsg[n])

    node = dot.Node('"' + n + '"', style="filled",
                    fillcolor=bgcol,
                    fontcolor=fgcol,
                    tooltip='"({0}) {1}{2}"'.format(bn.idFromName(n), n, res))
    graph.add_node(node)

  for a in bn.arcs():
    if arcWidth is None:
      pw = 1
      av = ""
    else:
      if a in arcWidth:
        if maxarcs == minarcs:
          pw = 1
        else:
          pw = 0.1 + 5 * (arcWidth[a] - minarcs) / (maxarcs - minarcs)
        av = arcWidth[a]
      else:
        pw = 1
        av = 1
    if arcColor is None:
      col = getBlackInTheme()
    else:
      if a in arcColor:
        col = _proba2color(arcColor[a], cmapArc)
      else:
        col = getBlackInTheme()

    edge = dot.Edge('"' + bn.variable(a[0]).name() + '"', '"' + bn.variable(a[1]).name() + '"',
                    penwidth=pw, color=col,
                    tooltip="{} : {}".format(a, av))
    graph.add_edge(edge)

  graph.set_size(size)
  return graph


def _stats(p):
  mu = 0.0
  mu2 = 0.0
  v = p.variable(0)
  for i, p in enumerate(p.tolist()):
    x = v.numerical(i)
    mu += p * x
    mu2 += p * x * x
  return (mu, math.sqrt(mu2 - mu * mu))


def _getTitleHisto(p):
  var = p.variable(0)
  if var.varType() == 1:  # Labelized
    return "{}".format(var.name())

  (mu, std) = _stats(p)
  return "{}\n$\mu={:.2f}$; $\sigma={:.2f}$".format(var.name(), mu, std)


def _getProbaV(p, scale=1.0):
  """
  compute the representation of an histogram for a mono-dim Potential

  :param p: the mono-dim Potential
  :return: a matplotlib bar (vertical histogram) for a Potential p.

  """
  var = p.variable(0)
  ra = np.arange(var.domainSize())

  fig = plt.figure()
  fig.set_figwidth(scale * var.domainSize() / 4.0)
  fig.set_figheight(scale * 2)

  ax = fig.add_subplot(111)

  bars = ax.bar(ra, p.tolist(), align='center')
  ax.set_ylim(bottom=0)
  ax.set_xticks(ra)
  ax.set_xticklabels(["{:.1%}".format(bar.get_height()) for bar in bars], rotation='vertical')
  ax.set_title(_getTitleHisto(p))
  ax.get_yaxis().grid(True)
  return fig


def _getProbaH(p, scale=1.0):
  """
  compute the representation of an histogram for a mono-dim Potential

  :param p: the mono-dim Potential
  :return: a matplotlib barh (horizontal histogram) for a Potential p.
  """
  var = p.variable(0)
  ra = np.arange(var.domainSize())
  ra_reverse = np.arange(var.domainSize() - 1, -1, -1)  # reverse order
  vx = ["{0}".format(var.label(int(i))) for i in ra_reverse]

  fig = plt.figure()
  fig.set_figheight(scale * var.domainSize() / 4.0)
  fig.set_figwidth(scale * 2)

  ax = fig.add_subplot(111)

  vals = p.tolist()
  vals.reverse()
  bars = ax.barh(ra, vals, align='center')

  for bar in bars:
    txt = "{:.1%}".format(bar.get_width())
    ax.text(1, bar.get_y(), txt, ha='right', va='bottom')

  ax.set_xlim(0, 1)
  ax.set_yticks(np.arange(var.domainSize()))
  ax.set_yticklabels(vx)
  ax.set_xticklabels([])
  # ax.set_xlabel('Probability')
  ax.set_title(_getTitleHisto(p))
  ax.get_xaxis().grid(True)
  return fig


def proba2histo(p, scale=1.0):
  """
  compute the representation of an histogram for a mono-dim Potential

  :param pyAgrum.Potential p: the mono-dim Potential
  :return: a matplotlib histogram for a Potential p.
  """
  if p.variable(0).domainSize() > 8:
    return _getProbaV(p, scale)
  else:
    return _getProbaH(p, scale)


def _saveFigProba(p, filename, format="svg"):
  fig = proba2histo(p)
  fig.savefig(filename, bbox_inches='tight', transparent=True, pad_inches=0.05, dpi=fig.dpi, format=format)
  plt.close(fig)


def BNinference2dot(bn, size="4", engine=None, evs={}, targets={}, format='png', nodeColor=None, arcWidth=None, arcColor=None,cmapNode=None, cmapArc=None):
  """
  create a pydotplus representation of an inference in a BN

  :param pyAgrum.BayesNet bn:
  :param string size: size of the rendered graph
  :param pyAgrum Inference engine: inference algorithm used. If None, LazyPropagation will be used
  :param dictionnary evs: map of evidence
  :param set targets: set of targets. If targets={} then each node is a target
  :param string format: render as "png" or "svg"
  :param nodeColor: a nodeMap of values to be shown as color nodes (with special color for 0 and 1)
  :param arcWidth: a arcMap of values to be shown as bold arcs
  :param arcColor: a arcMap of values (between 0 and 1) to be shown as color of arcs
  :param cmapNode: color map to show the vals of Nodes
  :param cmapArc: color map to show the vals of Arcs
  
  :return: the desired representation of the inference
  """
  if cmapNode is None:
    cmapNode = plt.get_cmap('summer')

  if cmapArc is None:
    cmapArc = plt.get_cmap('BuGn')

  if arcWidth is not None:
    minarcs = min(arcWidth.values())
    maxarcs = max(arcWidth.values())

  startTime = time.time()
  if engine is None:
    ie = gum.LazyPropagation(bn)
  else:
    ie = engine
  ie.setEvidence(evs)
  ie.makeInference()
  stopTime = time.time()

  from tempfile import mkdtemp
  temp_dir = mkdtemp("", "tmp", None)  # with TemporaryDirectory() as temp_dir:

  dotstr = "digraph structs {\n  fontcolor=\"" +  getBlackInTheme()+"\";bgcolor=\"transparent\";"
  dotstr += "  label=\"Inference in {:6.2f}ms\";\n".format(1000 * (stopTime - startTime))
  dotstr += "  node [fillcolor=floralwhite, style=filled,color=grey];\n"
  dotstr += '  edge [color="'+getBlackInTheme()+'"];'+"\n"

  for nid in bn.nodes():
    name = bn.variable(nid).name()

    # defaults
    bgcol = "#404040"
    fgcol = "#FFFFFF"
    if len(targets) == 0 or name in targets or nid in targets:
      bgcol = "white"

    if nodeColor is not None:
      if name in nodeColor or nid in nodeColor:
        bgcol = _proba2bgcolor(nodeColor[name], cmapNode)
        fgcol = _proba2fgcolor(nodeColor[name], cmapNode)
        
    # 'hard' colour for evidence (?)
    if name in evs or nid in evs:
      bgcol = "sandybrown"
      fgcol = "black"    

    colorattribute = 'fillcolor="{}", fontcolor="{}", color="#000000"'.format(bgcol, fgcol)
    if len(targets) == 0 or name in targets or nid in targets:
      filename = temp_dir + hashlib.md5(name.encode()).hexdigest() + "." + format
      _saveFigProba(ie.posterior(name), filename, format=format)
      dotstr += ' "{0}" [shape=rectangle,image="{1}",label="", {2}];\n'.format(name, filename, colorattribute)
    else:
      dotstr += ' "{0}" [{1}]'.format(name, colorattribute)

  for a in bn.arcs():
    (n, j) = a
    if arcWidth is None:
      pw = 1
      av = ""
    else:
      if (n, j) in arcWidth:
        if maxarcs == minarcs:
          pw = 1
        else:
          pw = 0.1 + 5 * (arcWidth[a] - minarcs) / (maxarcs - minarcs)
        av = arcWidth[a]
      else:
        pw = 1
        av = ""

    if arcColor is None:
      col = getBlackInTheme()
    else:
      if a in arcColor:
        col = _proba2color(arcColor[a], cmapArc)
      else:
        col = getBlackInTheme()

    dotstr += ' "{0}"->"{1}" [penwidth="{2}",tooltip="{3}:{4}",color="{5}"];'.format(bn.variable(n).name(), bn.variable(j).name(), pw, a, av,col)
  dotstr += '}'

  g = dot.graph_from_dot_data(dotstr)

  g.set_size(size)
  return g


def dotize(aBN, name, format='pdf'):
  """
  From a bn, creates an image of the BN

  :param pyAgrum.BayesNet bn: the bayes net to show
  :param string name: the filename (without extension) for the image
  :param string format: format in ['pdf','png','fig','jpg','svg']
  """
  if format not in ['pdf', 'png', 'fig', 'jpg', 'svg']:
    raise Exception("<%s> in not a correct style ([pdf,png,fig,jpg,svg])" % style)

  if isinstance(aBN, str):
    bn = gum.loadBN(aBN)
  else:
    bn = aBN

  imgfile = name + '.' + format
  BN2dot(bn).write(imgfile, format=format)


def pngize(aBN, name):
  """
  From a bn, creates a png of the BN

  :param pyAgrum.BayesNet bn: the bayes net to show
  :param string name: the filename (without extension) for the image
  """
  dotize(aBN, name, 'png')


def pdfize(aBN, name):
  """
  From a bn, creates a pdf of the BN

  :param pyAgrum.BayesNet bn: the bayes net to show
  :param string name: the filename (without extension) for the image
  """
  dotize(aBN, name, 'pdf')


if __name__ == "__main__":
  pyAgrum_header("2011-19")
  if len(sys.argv) < 2:
    print(os.path.basename(sys.argv[0]), "file.{" + gum.availableBNExts() + "}")
  else:
    base, ext = os.path.splitext(sys.argv[1])
    pdfize(sys.argv[1], base)

