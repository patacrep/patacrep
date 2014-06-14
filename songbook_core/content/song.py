#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import jinja2
import logging
import os

from songbook_core.content import Content, process_content, ContentError
from songbook_core.files import recursive_find
from songbook_core.songs import Song

LOGGER = logging.getLogger(__name__)

class SongRenderer(Content, Song):
    def begin_new_block(self, previous, __context):
        return not isinstance(previous, SongRenderer)

    def begin_block(self, context):
        indexes = context.resolve("indexes")
        if isinstance(indexes, jinja2.runtime.Undefined):
            indexes = ""
        return r'\begin{songs}{%s}' % indexes

    def end_block(self, __context):
        return r'\end{songs}'

    def render(self, context):
        outdir = os.path.dirname(context['filename'])
        if os.path.abspath(self.path).startswith(os.path.abspath(outdir)):
            path = os.path.relpath(self.path, outdir)
        else:
            path = os.path.abspath(self.path)
        return r'\input{{{}}}'.format(path)

def parse(keyword, argument, contentlist, config):
    if 'languages' not in config:
        config['languages'] = set()
    songlist = []
    if not contentlist:
        contentlist = [
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
    for elem in contentlist:
        before = len(songlist)
        for songdir in [os.path.join(d, 'songs') for d in config['datadir']]:
            for filename in glob.iglob(os.path.join(songdir, elem)):
                LOGGER.debug('Parsing file "{}"…'.format(filename))
                song = SongRenderer(filename, config)
                songlist.append(song)
                config["languages"].update(song.languages)
            if len(songlist) > before:
                break
        if len(songlist) == before:
            # No songs were added
            LOGGER.warning(
                    "Expression '{}' did not match any file".format(elem)
                    )
    return songlist


CONTENT_PLUGINS = {'song': parse}


class OnlySongsError(ContentError):
    def __init__(self, not_songs):
        self.not_songs = not_songs

    def __str__(self):
        return "Only songs are allowed, and the following items are not:" + str(not_songs)

def process_songs(content, config = None):
    contentlist = process_content(content, config)
    not_songs = [item for item in contentlist if not isinstance(item, SongRenderer)]
    if not_songs:
        raise OnlySongsError(not_songs)
    return contentlist
