"""Add a path directory to the 'songdir' list."""

from patacrep.content import process_content, validate_parser_argument
from patacrep.songs import DataSubpath

#pylint: disable=unused-argument
@validate_parser_argument("""
type: //rec
optional:
  content: //any
required:
  path: //str
""")
def parse(keyword, config, argument):
    """Return a list of songs, whith an another base path.

    Arguments:
    - keyword: unused;
    - config: the current songbook configuration dictionary;
    - argument: a dict containing:
        path: string specifying the path to add to the songdirs list;
        content: songbook content, that is parsed by
            patacrep.content.process_content().

    This function adds 'path' to the directories where songs are searched
    for, and then processes the content.

    The 'path' is added as a relative path to the dir of the songbook file.
    """
    subpath = argument['path']
    old_songdir = config['_songdir']

    config['_songdir'] = [DataSubpath(config['_songbookfile_dir'], subpath)]
    config['_songdir'].extend(old_songdir)

    processed_content = process_content(argument.get('content'), config)
    config['_songdir'] = old_songdir
    return processed_content

CONTENT_PLUGINS = {'addsongdir': parse}
