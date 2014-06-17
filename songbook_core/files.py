#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""File system utilities."""

import fnmatch
import os

def recursive_find(root_directory, pattern):
    """Recursively find files matching a pattern, from a root_directory.

    Return a list of files matching the pattern.
    """
    matches = []
    for root, _, filenames in os.walk(root_directory):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches

def relpath(path, start=None):
    """Return relative filepath to path if a subpath of start."""
    if start is None:
        start = os.curdir
    if os.path.abspath(path).startswith(os.path.abspath(start)):
        return os.path.relpath(path, start)
    else:
        return os.path.abspath(path)
