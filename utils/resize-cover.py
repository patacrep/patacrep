#!/usr/bin/python
# -*- coding: utf-8 -*-

#Author: Romain Goffe
#Date: 28/12/2011
#Description: Resize all covers to 128,128 thumbnails

import Image
import glob

width  = 128
height = 128

# Process song files
covers = glob.glob('songs/*/*.jpg')
for filename in covers:
    source = Image.open(filename)
    if source.size > (128, 128):
        print "resizing : " + filename
        target = source.resize((width, height), Image.ANTIALIAS)
        target.save(filename)
