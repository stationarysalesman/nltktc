# Natural Language Toolkit: graphical representations package
#
# Copyright (C) 2001-2016 NLTK Project
# Author: Edward Loper <edloper@gmail.com>
#         Steven Bird <stevenbird1@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

# Import Tkinter-based modules if Tkinter is installed
import nltktc.compat
try:
    import tkinter
except ImportError:
    import warnings
    warnings.warn("nltk.draw package not loaded "
                  "(please install Tkinter library).")
else:
    from nltktc.draw.cfg import ProductionList, CFGEditor, CFGDemo
    from nltktc.draw.tree import (TreeSegmentWidget, tree_to_treesegment,
                                  TreeWidget, TreeView, draw_trees)
    from nltktc.draw.table import Table

from nltktc.draw.dispersion import dispersion_plot

# skip doctests from this package
def setup_module(module):
    from nose import SkipTest
    raise SkipTest("nltk.draw examples are not doctests")
