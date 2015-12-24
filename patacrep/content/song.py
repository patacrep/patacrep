"""Plugin to include songs to the songbook."""

import glob
import jinja2
import logging
import os
import textwrap

from patacrep.content import process_content
from patacrep.content import ContentError, ContentItem, ContentList
from patacrep import files, errors

LOGGER = logging.getLogger(__name__)

class SongRenderer(ContentItem):
    """Render a song in as a tex code."""

    def __init__(self, song):
        super().__init__()
        self.song = song

    def iter_errors(self):
        """Iterate over song errors."""
        yield from self.song.errors

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

    #pylint: disable=unused-argument
    def render(self, context):
        """Return the string that will render the song."""
        return textwrap.dedent("""\
                {separator}
                %% {path}

                {song}
                """).format(
                    separator="%"*80,
                    path=files.path2posix(self.song.subpath),
                    song=self.song.render(),
                )

    def __lt__(self, other):
        """Order by song path"""
        return self.song.fullpath < other.song.fullpath

#pylint: disable=unused-argument
def parse(keyword, argument, contentlist, config):
    """Parse data associated with keyword 'song'.

    Arguments:
    - keyword: unused;
    - argument: unused;
    - contentlist: a list of strings, which are interpreted as regular
      expressions (interpreted using the glob module), referring to songs.
    - config: the current songbook configuration dictionary.

    Return a list of Song() instances.
    """
    plugins = config['_song_plugins']
    if '_langs' not in config:
        config['_langs'] = set()
    songlist = ContentList()
    for songdir in config['_songdir']:
        if contentlist:
            break
        contentlist = files.recursive_find(songdir.fullpath, plugins.keys())
    for elem in contentlist:
        before = len(songlist)
        for songdir in config['_songdir']:
            if not os.path.isdir(songdir.datadir):
                continue
            with files.chdir(songdir.datadir):
                for filename in glob.iglob(os.path.join(songdir.subpath, elem)):
                    LOGGER.debug('Parsing file "{}"…'.format(filename))
                    extension = filename.split(".")[-1]
                    if extension not in plugins:
                        songlist.append_error(ContentError(message=(
                                'I do not know how to parse "{}": name does '
                                'not end with one of {}. Ignored.'
                            ).format(
                                os.path.join(songdir.datadir, filename),
                                ", ".join(["'.{}'".format(key) for key in plugins.keys()]),
                                )))
                        continue
                    try:
                        renderer = SongRenderer(plugins[extension](
                            filename,
                            config,
                            datadir=songdir.datadir,
                            ))
                    except ContentError as error:
                        songlist.append_error(error)
                        continue
                    songlist.append(renderer)
                    config["_langs"].add(renderer.song.lang)
            if len(songlist) > before:
                break
        if len(songlist) == before:
            # No songs were added
            LOGGER.warning(errors.notfound(
                elem,
                [item.fullpath for item in config['_songdir']],
                message='Ignoring "{name}": did not match any file in {paths}.',
                ))
    return sorted(songlist)


CONTENT_PLUGINS = {'song': parse}


class OnlySongsError(ContentError):
    "A list that should contain only songs also contain other type of content."
    def __init__(self, not_songs):
        self.not_songs = not_songs
        super().__init__('song', str(self))

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
