#!/usr/bin/env python
# -*- coding: utf-8 -*-

import locale

from songbook_core.content.song import OnlySongsError, process_songs

DEFAULT_SORT = ['by', 'album', '@title']

def key_generator(sort):
    def ordered_song_keys(song):
        songkey = []
        for key in sort:
            if key == "@title":
                songkey.append(song.normalized_titles)
            elif key == "@path":
                songkey.append(locale.strxfrm(song.path))
            elif key == "by":
                songkey.append(song.normalized_authors)
            else:
                songkey.append(locale.strxfrm(song.args.get(key, "")))
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
