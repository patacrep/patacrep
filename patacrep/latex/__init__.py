"""Very simple LaTeX parser

This module uses an LALR parser to try to parse LaTeX code. LaTeX language
*cannot* be parsed by an LALR parser, so this is a very simple attemps, which
will work on simple cases, but not on complex ones.
"""

from patacrep.latex.syntax import tex2plain
from patacrep.latex.syntax import parsesong as syntax_parsesong
from patacrep import encoding

def parsesong(path, fileencoding=None):
    """Return a dictonary of data read from the latex file `path`.

    """
    with encoding.open_read(path, encoding=fileencoding) as songfile:
        data = syntax_parsesong(songfile.read(), path)
    data['@path'] = path
    return data
