#!/usr/bin/env python
# -*- coding: utf-8 -*-

import locale

from songbook_core.content.song import OnlySongsError, process_songs

DEFAULT_SORT = ['by', 'album', '@title']

def normalize_string(string):
    return locale.strxfrm(string.lower().strip())

def normalize_field(field):
    if isinstance(field, basestring):
        return normalize_string(field)
    elif isinstance(field, list):
        return [normalize_string(string) for string in field]

def key_generator(sort):
    def ordered_song_keys(song):
        songkey = []
        for key in sort:
            if key == "@title":
                field = song.unprefixed_titles
            elif key == "@path":
                field = song.path
            elif key == "by":
                field = song.authors
            else:
                field = song.args.get(key, "")
            songkey.append(normalize_field(field))
        return songkey
    return ordered_song_keys

def parse(keyword, config, argument, contentlist):
    if argument:
        sort = [key.strip() for key in argument.split(",")]
    else:
        sort = DEFAULT_SORT
    try:
        songlist = process_songs(contentlist, config)
    except OnlySongsError as error:
        raise ContentError(keyword, "Content list of this keyword can bo only songs (or content that result into songs), and the following are not:" + str(error.not_songs))
    return sorted(songlist, key=key_generator(sort))

CONTENT_PLUGINS = {'sorted': parse}
