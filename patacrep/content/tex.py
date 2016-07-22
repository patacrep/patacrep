"""Include LaTeX raw code in the songbook."""

import logging
import os

from patacrep import files, errors
from patacrep.content import ContentItem, ContentList, ContentError, validate_parser_argument

LOGGER = logging.getLogger(__name__)

class LaTeX(ContentItem):
    """Inclusion of LaTeX code"""

    def __init__(self, filename):
        self.filename = filename

    def render(self, context):
        return r'\input{{{}}}'.format(files.path2posix(files.relpath(
            self.filename,
            os.path.dirname(context['filename']),
            )))

    def to_dict(self):
        return {'tex': self.filename}

#pylint: disable=unused-argument
@validate_parser_argument("""
type: //any
of:
  - type: //arr
    contents: //str
  - type: //str
""")
def parse(keyword, argument, config):
    """Parse the tex files.

    Arguments:
    - keyword: unused;
    - argument:
        a list of tex files to include
        or a string of the tex file to include;
    - config: configuration dictionary of the current songbook.
    """
    if isinstance(argument, str):
        argument = [argument]

    filelist = ContentList()
    basefolders = [path.fullpath for path in config['_songdir']] + list(
        files.iter_datadirs(config['_datadir'], 'latex')
        )
    for filename in argument:
        checked_file = None
        for path in basefolders:
            if os.path.exists(os.path.join(path, filename)):
                checked_file = os.path.relpath(os.path.join(
                    path,
                    filename,
                    ))
                break
        if not checked_file:
            filelist.append_error(
                ContentError(
                    keyword="tex",
                    message=errors.notfound(filename, basefolders),
                    )
                )
            continue
        filelist.append(LaTeX(checked_file))

    return filelist

CONTENT_PLUGINS = {'tex': parse}
