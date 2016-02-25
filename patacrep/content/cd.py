"""Change base directory before importing songs."""

from patacrep.content import process_content, validate_parser_argument
from patacrep.songs import DataSubpath

#pylint: disable=unused-argument
@validate_parser_argument("""
type: //rec
required:
  path: //str
optional:
  content: //any
  yaml_as_root: //bool
""")
def parse(keyword, config, argument):
    """Return a list songs, whith a different base path.

    Arguments:
    - keyword: unused;
    - config: the current songbook configuration dictionary;
    - argument: a dict containing:
        path: string specifying the path to use as root;
        yaml_as_root: (optional) if the yaml file folder should
            be used as root folder
        content: songbook content, that is parsed by
            patacrep.content.process_content().

    This function adds 'path' to the directories where songs are searched
    for, and then processes the content.

    If 'yaml_as_root' is not set the 'path' is added as a relative path to
    every path already present in config['songdir'] (which are 'songs' dir
     inside the datadirs).
    Otherwise only the 'path' folder of the yaml file is insert as first
    folder to search into.
    """
    subpath = argument['path']
    old_songdir = config['_songdir']

    if argument.get('yaml_as_root', False):
        config['_songdir'].insert(0, DataSubpath(config['_songbookfile_dir'], subpath))
    else:
        config['_songdir'] = [path.clone().join(subpath) for path in config['_songdir']]

    processed_content = process_content(argument.get('content'), config)
    config['_songdir'] = old_songdir
    return processed_content

CONTENT_PLUGINS = {'cd': parse}
