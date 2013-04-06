#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import re

reTitle  = re.compile('(?<=beginsong\\{)(.(?<!\\}]))+')
reArtist = re.compile('(?<=by=)(.(?<![,\\]\\}]))+')
reAlbum  = re.compile('(?<=album=)(.(?<![,\\]\\}]))+')
#reLilypond  = re.compile('(?<=album=)(.(?<![,\\]\\}]))+')

class Song:
    def __init__(self, title, artist, album, path, isLilypond):
        self.title  = title
        self.artist = artist
        self.album  = album
        self.path   = path
        self.isLilypond = isLilypond
    def __repr__(self):
        return repr((self.title, self.artist, self.album, self.path, self.isLilypond))

