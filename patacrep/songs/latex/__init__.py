"""Very simple LaTeX parser

This module uses an LALR parser to try to parse LaTeX code. LaTeX language
*cannot* be parsed by an LALR parser, so this is a very simple attemps, which
will work on simple cases, but not on complex ones.
"""

import os

from patacrep import files, encoding
from patacrep.latex import parse_song, BABEL_LANGUAGES
from patacrep.songs import Song

class Latex2LatexSong(Song):
    """Song written in LaTeX, rendered in LaTeX"""
    # pylint: disable=abstract-method

    def _parse(self):
        """Parse content, and return the dictionary of song data."""
        with encoding.open_read(self.fullpath, encoding=self.encoding) as song:
            self.data = parse_song(song.read(), self.fullpath)
        self.titles = self.data['@titles']
        del self.data['@titles']
        self.set_lang(self.data['@language'])
        del self.data['@language']
        if "by" in self.data:
            self.authors = [self.data['by']]
            del self.data['by']
        else:
            self.authors = []

    def render(self, *args, **kwargs):
        """Return the code rendering the song."""
        # pylint: disable=signature-differs
        filename = os.path.basename(self.fullpath)
        path = os.path.abspath(os.path.dirname(self.fullpath))
        return r'\import{{{}/}}{{{}}}'.format(files.path2posix(path), filename)

    def set_lang(self, language):
        """Set the language code"""
        for lang, babel_language in BABEL_LANGUAGES.items():
            if language == babel_language:
                self.lang = lang
                return

        # Add a custom language to the babel dictionary (language is not officially supported)
        custom_lang = '_' + language
        BABEL_LANGUAGES[custom_lang] = language
        self.lang = custom_lang

SONG_RENDERERS = {
    "tsg": {
        'tis': Latex2LatexSong,
        'tsg': Latex2LatexSong,

        # For backward compatibility
        'sg': Latex2LatexSong,
    },
}
