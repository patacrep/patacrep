"""Dumb and very very incomplete LaTeX parser.

This module uses an LALR parser to try to parse LaTeX code. LaTeX language
*cannot* be parsed by an LALR parser, so this is a very simple attemps, which
will work on simple cases, but not on complex ones.
"""

import logging
from collections import OrderedDict

from patacrep.latex.syntax import tex2plain, parse_song

LOGGER = logging.getLogger(__name__)

BABEL_LANGUAGES = OrderedDict((
    ('fr', 'french'),
    ('en', 'english'),
    ('de', 'german'),
    ('es', 'spanish'),
    ('it', 'italian'),
    ('pt', 'portuguese'),
))

def lang2babel(lang):
    """Return the language used by babel, corresponding to the language code"""
    try:
        return BABEL_LANGUAGES[lang]
    except KeyError:
        available = ", ".join(BABEL_LANGUAGES.keys())
        LOGGER.error('Unknown lang code: ' + lang + '. Supported: ' + available)
        return 'english'

def latexpath(path):
    """In LaTeX paths use '/' even on windows"""
    return path.replace('\\', '/')
