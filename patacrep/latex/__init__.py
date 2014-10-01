# -*- coding: utf-8 -*-

"""Very simple LaTeX parser

This module uses an LALR parser to try to parse LaTeX code. LaTeX language
*cannot* be parsed by an LALR parser, so this is a very simple attemps, which
will work on simple cases, but not on complex ones.
"""

from patacrep.latex.syntax import tex2plain as syntax_tex2plain
from patacrep.latex.syntax import parsesong as syntax_parsesong
from patacrep.latex.detex import detex
from patacrep import encoding

def tex2plain(string):
    """Render LaTeX string

    Very few commands (mostly diacritics) are interpreted.
    """
    return syntax_tex2plain(string)

def parsesong(path):
    """Return a dictonary of data read from the latex file `path`.

    """
    data = syntax_parsesong(encoding.open_read(path).read(), path)
    data['@path'] = path
    return data
