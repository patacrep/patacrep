"""Dumb and very very incomplete LaTeX parser.

This module uses an LALR parser to try to parse LaTeX code. LaTeX language
*cannot* be parsed by an LALR parser, so this is a very simple attemps, which
will work on simple cases, but not on complex ones.
"""

from patacrep.latex.syntax import tex2plain, parse_song
