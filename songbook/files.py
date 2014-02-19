#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""File system utilities."""

import fnmatch
import os

def recursiveFind(root_directory, pattern):
    """Recursively find files matching a pattern, from a root_directory.

    Return a list of files matching the pattern.
    """
    matches = []
    for root, dirnames, filenames in os.walk(root_directory):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches
