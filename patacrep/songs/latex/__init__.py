"""Very simple LaTeX parser

This module uses an LALR parser to try to parse LaTeX code. LaTeX language
*cannot* be parsed by an LALR parser, so this is a very simple attemps, which
will work on simple cases, but not on complex ones.
"""

import os

from patacrep import files, encoding
from patacrep.latex import parse_song
from patacrep.songs import Song

class Latex2LatexSong(Song):
    """Song written in LaTeX, rendered in LaTeX"""
    # pylint: disable=abstract-method

    def _parse(self, __config):
        """Parse content, and return the dictinory of song data."""
        with encoding.open_read(self.fullpath, encoding=self.encoding) as song:
            self.data = parse_song(song.read(), self.fullpath)
        self.titles = self.data['@titles']
        del self.data['@titles']
        self.languages = self.data['@languages']
        del self.data['@languages']
        if "by" in self.data:
            self.authors = [self.data['by']]
            del self.data['by']
        else:
            self.authors = []

    def render(self, output):
        """Return the code rendering the song."""
        # pylint: disable=signature-differs
        if output is None:
            raise ValueError(output)
        path = files.path2posix(files.relpath(
            self.fullpath,
            os.path.dirname(output)
        ))
        return r'\import{{{}/}}{{{}}}'.format(os.path.dirname(path), os.path.basename(path))

SONG_RENDERERS = {
    "latex": {
        'is': Latex2LatexSong,
        'sg': Latex2LatexSong,
    },
}
