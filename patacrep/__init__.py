"""Global variables."""

import os
import sys

from pkg_resources import resource_filename

# Check Python version
if sys.version_info < (3, 3):
    print("ERROR: Your Python version is too old. Please use a Python version > 3.3.")
    sys.exit(1)

# Patacrep version.
__TUPLE_VERSION__ = (5, 2, 0)
__version__ = '.'.join([str(number) for number in __TUPLE_VERSION__])

# Directory containing shared data (default templates, custom LaTeX packages,
# etc.)

__DATADIR__ = os.path.abspath(resource_filename(__name__, 'data'))
def pkg_datapath(*path):
    """Return the package data path"""
    return os.path.join(__DATADIR__, *path)
