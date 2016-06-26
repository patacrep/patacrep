"""Sorted list of songs.

This plugin provides keyword 'sort', used to include a sorted list of songs
to a songbook.
"""

import logging

from patacrep import files
from patacrep.content import ContentError
from patacrep.content import process_content, validate_parser_argument
from patacrep.content.song import OnlySongsError
from patacrep.utils import normalize_string

LOGGER = logging.getLogger(__name__)

DEFAULT_SORT = ['by', 'album', 'title']

def normalize_field(field):
    """Return a normalized field, it being a string or a list of strings."""
    if isinstance(field, str):
        return normalize_string(field)
    elif isinstance(field, list) or isinstance(field, tuple):
        return [normalize_field(string) for string in field]

def key_generator(sort):
    """Return a function that returns the list of values used to sort the song.

    Arguments:
        - sort: the list of keys used to sort.
    """

    def ordered_song_keys(songrenderer):
        """Return the list of values used to sort the song."""
        song = songrenderer.song
        songkey = []
        for key in sort:
            if key == "title":
                field = song.unprefixed_titles
            elif key == "path":
                field = song.fullpath
            elif key == "by":
                field = song.authors
            else:
                try:
                    field = song.data[key]
                except KeyError:
                    LOGGER.debug(
                        "Ignoring missing key '{}' for song {}.".format(
                            key,
                            files.relpath(song.fullpath),
                            )
                        )
                    field = ""
            songkey.append(normalize_field(field))
        return songkey
    return ordered_song_keys

#pylint: disable=unused-argument
@validate_parser_argument("""
type: //any
of:
  - type: //nil
  - type: //rec
    optional:
      key:
        type: //any
        of:
          - //str
          - type: //arr
            contents: //str
      content: //any
""")
def parse(keyword, config, argument):
    """Return a sorted list of songs.

    Arguments:
        - keyword: the string 'sort';
        - config: the current songbook configuration dictionary;
        - argument: a dict of:
            key: the list of the fields used to sort songs (e.g. "by", "album", "title")
            content: content to be sorted. If this content
                contain something else than a song, an exception is raised.
    """
    if argument is None:
        argument = {}
    sort = argument.get('key', DEFAULT_SORT)
    if isinstance(sort, str):
        sort = [sort]
    try:
        songlist = process_content(argument.get('content'), config)
    except OnlySongsError as error:
        raise ContentError(keyword, (
            "Content list of this keyword can be only songs (or content "
            "that result into songs), and the following are not:" +
            str(error.not_songs)
            ))
    return sorted(songlist, key=key_generator(sort))

CONTENT_PLUGINS = {'sort': parse}
