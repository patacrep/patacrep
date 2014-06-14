#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import jinja2
import os

from songbook_core.content import Content
from songbook_core.files import recursive_find

class Song(Content):
    def __init__(self, filename):
        self.filename = filename

    def begin_new_block(self, previous, __context):
        return not isinstance(previous, Song)

    def begin_block(self, context):
        indexes = context.resolve("indexes")
        if isinstance(indexes, jinja2.runtime.Undefined):
            indexes = ""
        return r'\begin{songs}{%s}' % indexes

    def end_block(self, __context):
        return r'\end{songs}'

    def render(self, __context):
        return r'\input{{{}}}'.format(self.filename)

def parse(keyword, config, *arguments):
    songlist = []
    if not arguments:
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
