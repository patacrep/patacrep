#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Plugin to include songs to the songbook."""

import glob
import jinja2
import logging
import os

from patacrep.content import Content, process_content, ContentError
from patacrep import files
from patacrep.songs import Song

LOGGER = logging.getLogger(__name__)

class SongRenderer(Content, Song):
    """Render a song in the .tex file."""

    def begin_new_block(self, previous, __context):
        """Return a boolean stating if a new block is to be created."""
        return not isinstance(previous, SongRenderer)

    def begin_block(self, context):
        """Return the string to begin a block."""
        indexes = context.resolve("indexes")
        if isinstance(indexes, jinja2.runtime.Undefined):
            indexes = ""
        return r'\begin{songs}{%s}' % indexes

    def end_block(self, __context):
        """Return the string to end a block."""
        return r'\end{songs}'

    def render(self, context):
        """Return the string that will render the song."""
        return r'\input{{{}}}'.format(files.relpath(
            self.path,
            os.path.dirname(context['filename'])
            ))

#pylint: disable=unused-argument
def parse(keyword, argument, contentlist, config):
    """Parse data associated with keyword 'song'.

    Arguments:
    - keyword: unused;
    - argument: unused;
    - contentlist: a list of strings, which are interpreted as regular
      expressions (interpreted using the glob module), referring to songs.
    - config: the current songbook configuration dictionary.

    Return a list of SongRenderer() instances.
    """
    if 'languages' not in config:
        config['_languages'] = set()
    songlist = []
    for songdir in config['_songdir']:
        if contentlist:
            break
        contentlist = [
                files.relpath(filename, songdir)
                for filename
                in files.recursive_find(songdir, "*.sg")
                ]
    for elem in contentlist:
        before = len(songlist)
        for songdir in config['_songdir']:
            for filename in glob.iglob(os.path.join(songdir, elem)):
                LOGGER.debug('Parsing file "{}"…'.format(filename))
                song = SongRenderer(filename, config)
                songlist.append(song)
                config["_languages"].update(song.languages)
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
    "A list that should contain only songs also contain other type of content."
    def __init__(self, not_songs):
        super(OnlySongsError, self).__init__()
        self.not_songs = not_songs

    def __str__(self):
        return (
                "Only songs are allowed, and the following items are not:" +
                str(self.not_songs)
                )

def process_songs(content, config=None):
    """Process content that containt only songs.

    Call patacrep.content.process_content(), checks if the returned list
    contains only songs, and raise an exception if not.
    """
    contentlist = process_content(content, config)
    not_songs = [
            item
            for item
            in contentlist
            if not isinstance(item, SongRenderer)
            ]
    if not_songs:
        raise OnlySongsError(not_songs)
    return contentlist
