#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os

from songbook_core.content import Content
from songbook_core.files import recursive_find

class Song(Content):
    def __init__(self, filename):
        self.filename = filename

    def begin_new_block(self, previous):
        return not isinstance(previous, Song)

    def begin_block(self):
       #TODO index return r'\begin{songs}{((indexes|default("")))}'
       return r'\begin{songs}{titleidx,authidx}'

    def end_block(self):
        return r'\end{songs}'

    def render(self):
        return r'\input{{{}}}'.format(self.filename)

def parse(keyword, config, *arguments):
    songlist = []
    if not arguments:
        import ipdb; ipdb.set_trace()
        arguments = [
                os.path.relpath(
                    filename,
                    os.path.join(config['datadir'][0], 'songs'),
                    )
                for filename
                in recursive_find(
                    os.path.join(config['datadir'][0], 'songs'),
                    "*.sg"
                    )
                ]
    for elem in arguments:
        before = len(songlist)
        for songdir in [os.path.join(d, 'songs') for d in config['datadir']]:
            for filename in glob.iglob(os.path.join(songdir, elem)):
                songlist.append(Song(filename))
            if len(songlist) > before:
                break
        if len(songlist) == before:
            # No songs were added
            LOGGER.warning(
                    "Expression '{}' did not match any file".format(elem)
                    )
    return songlist


CONTENT_PLUGINS = {'song': parse}
