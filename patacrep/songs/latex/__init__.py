"""Very simple LaTeX parser

This module uses an LALR parser to try to parse LaTeX code. LaTeX language
*cannot* be parsed by an LALR parser, so this is a very simple attemps, which
will work on simple cases, but not on complex ones.
"""

import os

from patacrep import files
from patacrep.latex import parse_song
from patacrep.songs import Song

class LatexSong(Song):
    """LaTeX song parser."""

    def parse(self, content):
        """Parse content, and return the dictinory of song data."""
        return parse_song(content, self.fullpath)

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
