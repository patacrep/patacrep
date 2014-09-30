# -*- coding: utf-8 -*-

from patacrep.latex.syntax import tex2plain as syntax_tex2plain
from patacrep.latex.syntax import parsesong as syntax_parsesong
from patacrep.latex.detex import detex
from patacrep import encoding

"""Very simple LaTeX parser"""

def tex2plain(string):
    """Render LaTeX string

    Very few commands (mostly diacritics) are interpreted.
    """
    return syntax_tex2plain(string)

def parsesong(path):
    """Return a dictonary of data read from the latex file `path`.

    This file is a drop in replacement for an old function. Elle ne devrait pas
    apparaitre telle quelle dans la version finale, une fois que
    https://github.com/patacrep/patacrep/issues/64 aura été pris en compte.
    """
    data = syntax_parsesong(encoding.open_read(path).read(), path)
    data['@path'] = path
    return data
