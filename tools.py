#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import fnmatch
import os

def recursiveFind(root_directory, pattern):
   matches = []
   for root, dirnames, filenames in os.walk(root_directory):
      for filename in fnmatch.filter(filenames, pattern):
         matches.append(os.path.join(root, filename))
   return matches
