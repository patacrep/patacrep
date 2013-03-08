#!/usr/bin/python
# -*- coding: utf-8 -*-

#Author: Romain Goffe
#Date: 28/12/2011
#Description: Resize all covers to 128,128 thumbnails

import Image

from utils.utils import recursiveFind

# Process song files
covers = recursiveFind(os.path.join(library, 'songs'), '*.jpg')
for filename in covers:

    source = Image.open(filename)

    src_width = source.size[0]
    src_height = source.size[1]
    ratio = float(src_height) / float(src_width)

    width  = 128
    height = 128
    error  = 0.2 #0: always preserve ratio; 1: always square images 

    #tolerate almost square images
    if ratio < 1 - error  or ratio > 1 + error:
        #print "preserve ratio = ", ratio
        #preserve important ratio
        if src_width < src_height:
            height = int(width * ratio)
        elif src_height < src_width:
            width = int(height * ratio)

    if src_width > width and src_height > height:
        print "resize: ", filename, " from ", source.size, " to ", (width, height)
        target = source.resize((width, height), Image.ANTIALIAS)
        target.save(filename)
