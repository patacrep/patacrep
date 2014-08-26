"""Global variables."""

from pkg_resources import resource_filename
import os

# Version

__TUPLE_VERSION__ = (4, 0, 0, "alpha")
__version__ = '.'.join([str(number) for number in __TUPLE_VERSION__])

# Directory containing shared data (default templates, custom LaTeX packages,
# etc.)

__DATADIR__ = os.path.abspath(resource_filename(__name__, 'data'))
