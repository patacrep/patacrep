"""Very simple LaTeX parsing."""

import os

from patacrep import files
from patacrep.latex import parsesong
from patacrep.songs import Song

class TexRenderer(Song):
    """Renderer for song and intersong files."""

    def parse(self):
        """Parse song and set metadata."""
        self.data = parsesong(self.fullpath, self.encoding)
        self.titles = self.data['@titles']
        self.languages = self.data['@languages']
        self.authors = self.data['by']

    def render(self, context):
        """Return the string that will render the song."""
        return r'\input{{{}}}'.format(files.path2posix(
                                    files.relpath(
                                        self.fullpath,
                                        os.path.dirname(context['filename'])
                                    )))

FILE_PLUGINS = {
        'sg': TexRenderer,
        'is': TexRenderer,
        }
