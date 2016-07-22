"""Common functions for patatools"""

import argparse
import os

def existing_file(name):
    """Check that argument is an existing, readable file name.

    Return the argument for convenience.
    """
    if os.path.isfile(name) and os.access(name, os.R_OK):
        return name
    raise argparse.ArgumentTypeError("Cannot read file '{}'.".format(name))
