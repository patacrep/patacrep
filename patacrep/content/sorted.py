#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sorted list of songs.

This plugin provides keyword 'sorted', used to include a sorted list of songs
to a songbook.
"""

import locale
import logging

from patacrep import files
from patacrep.content import ContentError
from patacrep.content.song import OnlySongsError, process_songs

LOGGER = logging.getLogger(__name__)

DEFAULT_SORT = ['by', 'album', '@title']

def normalize_string(string):
    """Return a normalized string.

    Normalized means:
    - no surrounding spaces;
    - lower case;
    - passed through locale.strxfrm().
    """
    return locale.strxfrm(string.lower().strip())

def normalize_field(field):
    """Return a normalized field, it being a string or a list of strings."""
    if isinstance(field, basestring):
        return normalize_string(field)
    elif isinstance(field, list):
        return [normalize_string(string) for string in field]

def key_generator(sort):
    """Return a function that returns the list of values used to sort the song.

    Arguments:
        - sort: the list of keys used to sort.
    """

    def ordered_song_keys(song):
        """Return the list of values used to sort the song."""
        songkey = []
        for key in sort:
            if key == "@title":
                field = song.unprefixed_titles
            elif key == "@path":
                field = song.path
            elif key == "by":
                field = song.authors
            else:
                try:
                    field = song.args[key]
                except KeyError:
                    LOGGER.debug(
                            "Ignoring unknown key '{}' for song {}.".format(
                                key,
                                files.relpath(song.path),
                                )
                            )
                    field = ""
            songkey.append(normalize_field(field))
        return songkey
    return ordered_song_keys

#pylint: disable=unused-argument
def parse(keyword, config, argument, contentlist):
    """Return a sorted list of songs contained in 'contentlist'.

    Arguments:
        - keyword: the string 'sorted';
        - config: the current songbook configuration dictionary;
        - argument: the list of the fields used to sort songs, as strings
          separated by commas (e.g. "by, album, @title");
        - contentlist: the list of content to be sorted. If this content
          contain something else than a song, an exception is raised.
    """
    if argument:
        sort = [key.strip() for key in argument.split(",")]
    else:
        sort = DEFAULT_SORT
    try:
        songlist = process_songs(contentlist, config)
    except OnlySongsError as error:
        raise ContentError(keyword, (
            "Content list of this keyword can be only songs (or content "
            "that result into songs), and the following are not:" +
            str(error.not_songs)
            ))
    return sorted(songlist, key=key_generator(sort))

CONTENT_PLUGINS = {'sorted': parse}
