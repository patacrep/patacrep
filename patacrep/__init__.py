"""Global variables."""

from pkg_resources import resource_filename
import os

# Check Python version
import sys
if sys.version_info < (3, 3):
    print("ERROR: Your Python version is too old. Please use a Python version > 3.3.")
    sys.exit(1)

# Patacrep version.
__TUPLE_VERSION__ = (4, 0, 0)
__version__ = '.'.join([str(number) for number in __TUPLE_VERSION__])

# Directory containing shared data (default templates, custom LaTeX packages,
# etc.)

_ROOT = os.path.abspath(resource_filename(__name__, 'data'))
def pkg_datapath(path=''):
    """Return the package data path"""
    return os.path.join(_ROOT, path)

__DATADIR__ = os.path.abspath(pkg_datapath())
