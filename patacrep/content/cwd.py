"""Change base directory before importing songs."""

import os

from patacrep.content import process_content, validate_parser_argument
from patacrep.songs import DataSubpath

#pylint: disable=unused-argument
@validate_parser_argument("""
type: //rec
required:
  path: //str
optional:
  content: //any
""")
def parse(keyword, config, argument):
    """Return a list songs, whith a different base path.

    Arguments:
    - keyword: unused;
    - config: the current songbook configuration dictionary;
    - argument: a dict containing:
        path: string specifying the path to use as root;
        content: songbook content, that is parsed by
            patacrep.content.process_content().

    This function adds 'path' to the directories where songs are searched
    for, and then processes the content.

    The 'path' is added:
    - first as a relative path to the *.yaml file directory;
    - then as a relative path to every path already present in
      config['songdir'].
    """
    subpath = argument['path']
    old_songdir = config['_songdir']
    sbdir = os.path.dirname(config['_filepath'])

    config['_songdir'] = (
        [DataSubpath(sbdir, subpath)] +
        [path.clone().join(subpath) for path in config['_songdir']]
        )
    processed_content = process_content(argument.get('content'), config)
    config['_songdir'] = old_songdir
    return processed_content

CONTENT_PLUGINS = {'cwd': parse}
