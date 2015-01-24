"""Very simple LaTeX parser

This module uses an LALR parser to try to parse LaTeX code. LaTeX language
*cannot* be parsed by an LALR parser, so this is a very simple attemps, which
will work on simple cases, but not on complex ones.
"""

import os

from patacrep import files, encoding
from patacrep.latex import parse_song
from patacrep.songs import Song

class LatexSong(Song):
    """LaTeX song parser."""

    def parse(self, __config):
        """Parse content, and return the dictinory of song data."""
        with encoding.open_read(self.fullpath, encoding=self.encoding) as song:
            self.data = parse_song(song.read(), self.fullpath)
        self.titles = self.data['@titles']
        del self.data['@titles']
        self.languages = self.data['@languages']
        del self.data['@languages']
        self.authors = [self.data['by']]
        del self.data['by']

    def tex(self, output):
        """Return the LaTeX code rendering the song."""
        return r'\input{{{}}}'.format(files.path2posix(
                                    files.relpath(
                                        self.fullpath,
                                        os.path.dirname(output)
                                    )))

SONG_PARSERS = {
    'is': LatexSong,
    'sg': LatexSong,
    }
