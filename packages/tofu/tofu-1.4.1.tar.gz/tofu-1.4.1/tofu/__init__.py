"""
ToFu: A python library for Tomography for Fusion research
=========================================================

Provides
  1. Objects to handle 3D geometry of diagnostics
  2. Built-in methods for computing key quantities, data treatment, inversions...
  3. Visualisation tools

How to use the documentation
----------------------------
Documentation is available in two forms:
  1. Docstrings provided with the code
  2. A loose standing reference guide, available from `the ToFu homepage <http://www.tofu.org>`_.


Available subpackages
---------------------
geom
    Geometry-handling, with dedicated objects, methods and functions
mesh
    Mesh and basis functions creation and handling, as well as 2D equilibrium storing
matcomp
    Computation of geometry matrix from outputs of both geom and mesh
treat
    Data-handling objects and methods for pre-treatment (visualisation, treatment...)
inv
    Inversion-regularisation algortihms, using outputs from matcomp and data, plus visualisation

Available modules
-----------------
defaults
    Store most default parameters of tofu
pathfile
    Provide a class for identification of all tofu objects, and functions for path and file handling
helper
    miscellaneous helper functions

Utilities
---------
test
    Run tofu unittests
show_config
    Show tofu build configuration
__version__
    tofu version string


Created on Wed May 18 2016

@author: didiervezinet
@author_email: didier.vezinet@gmail.com
"""
import sys
import warnings
if sys.version[0] == '2':
    from .version import __version__
elif sys.version[0] == '3':
    from .version import __version__

# For tests without display with nosetests
if not 'matplotlib.pyplot' in sys.modules:
    import matplotlib
    matplotlib.use('agg')
    del matplotlib

import tofu.pathfile as pathfile
import tofu.utils as utils

from tofu.utils import save, load, load_from_imas, calc_from_imas
import tofu._plot as _plot
import tofu.geom as geom
import tofu.data as data


try:
    import tofu.imas2tofu as imas2tofu
    okimas2tofu = True
except Exception as err:
    warnings.warn(str(err))
    okimas2tofu = False

try:
    import tofu.mag as mag
    okmag = True
except Exception as err:
    warnings.warn(str(err))
    okmag = False

#import tofu.dust as dust


__all__ = ['pathfile','utils','_plot','geom','data']
if okimas2tofu:
    __all__.append('imas2tofu')
if okmag:
    __all__.append('mag')


del sys, warnings, okimas2tofu, okmag

#__all__.extend(['geom', 'mesh', 'matcomp', 'data', 'inv'])

#__name__ = ""
#__date__ = "$Mar 05, 2014$"
#__copyright__ = ""
#__license__ = ""
#__url__ = ""
#__path__ =
