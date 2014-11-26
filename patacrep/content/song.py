"""Plugin to include songs to the songbook."""

import glob
import logging
import os

from patacrep.content import process_content, ContentError
from patacrep import files, errors
from patacrep.songs import Song

LOGGER = logging.getLogger(__name__)

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
    if '_languages' not in config:
        config['_languages'] = set()
    songlist = []
    plugins = config.get('_file_plugins', {})
    for songdir in config['_songdir']:
        if contentlist:
            break
        contentlist = files.recursive_find(songdir.fullpath, plugins.keys())

    for elem in contentlist:
        before = len(songlist)
        for songdir in config['_songdir']:
            if songdir.datadir and not os.path.isdir(songdir.datadir):
                continue
            with files.chdir(songdir.datadir):
                for filename in glob.iglob(os.path.join(songdir.subpath, elem)):
                    LOGGER.debug('Parsing file "{}"…'.format(filename))
                    try:
                        renderer = plugins[filename.split('.')[-1]]
                    except KeyError:
                        LOGGER.warning((
                            'I do not know how to parse file "{}". Ignored.'
                            ).format(os.path.join(songdir.datadir, filename))
                            )
                        continue
                    song = renderer(songdir.datadir, filename, config)
                    songlist.append(song)
                    config["_languages"].update(song.languages)
            if len(songlist) > before:
                break
        if len(songlist) == before:
            # No songs were added
            LOGGER.warning(errors.notfound(
                elem,
                [item.fullpath for item in config['_songdir']],
                message='Ignoring "{name}": did not match any file in {paths}.',
                ))
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
            if not isinstance(item, Song)
            ]
    if not_songs:
        raise OnlySongsError(not_songs)
    return contentlist
