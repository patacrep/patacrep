"""Include LaTeX raw code in the songbook."""

import itertools
import logging
import os

from patacrep import files, errors
from patacrep.content import ContentItem, ContentList, ContentError

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

#pylint: disable=unused-argument
def parse(keyword, argument, contentlist, config):
    """Parse the contentlist.

    Arguments:
    - keyword: unused;
    - argument: unused;
    - contentlist: a list of name of tex files;
    - config: configuration dictionary of the current songbook.
    """
    if not contentlist:
        LOGGER.warning(
            "Useless 'tex' content: list of files to include is empty."
            )
    filelist = ContentList()
    basefolders = itertools.chain(
        (path.fullpath for path in config['_songdir']),
        files.iter_datadirs(config['_datadir']),
        files.iter_datadirs(config['_datadir'], 'latex'),
        )
    for filename in contentlist:
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
