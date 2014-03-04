"""Global variables."""

from pkg_resources import resource_filename
import os

# Version

__VERSION__ = (3, 7, 2)
__STR_VERSION__ = '.'.join([str(number) for number in __VERSION__])

# Directory containing shared data (default templates, custom LaTeX packages,
# etc.)

__DATADIR__ = os.path.abspath(resource_filename(__name__, 'data'))
