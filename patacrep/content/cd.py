"""Change base directory before importing songs."""

from patacrep.content import process_content, validate_parser_argument

#pylint: disable=unused-argument
@validate_parser_argument("""
type: //rec
required:
  path: //str
optional:
  content: //any
""")
def parse(keyword, config, argument):
    """Return a list of songs, whith a different base path.

    Arguments:
    - keyword: unused;
    - config: the current songbook configuration dictionary;
    - argument: a dict containing:
        path: string specifying the path to append to current songdirs;
        content: songbook content, that is parsed by
            patacrep.content.process_content().

    The 'path' is added as a relative path to every path already present
    in config['songdir'] (which are 'songs' dir inside the datadirs).
    """
    subpath = argument['path']
    old_songdir = config['_songdir']

    config['_songdir'] = [path.clone().join(subpath) for path in config['_songdir']]

    processed_content = process_content(argument.get('content'), config)
    config['_songdir'] = old_songdir
    return processed_content

CONTENT_PLUGINS = {'cd': parse}
