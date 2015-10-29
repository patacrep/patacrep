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
    ('de_de', 'german'),
    ('de_at', 'austrian'),
    ('eo_uy', 'esperanto'),
    ('en_us', 'english'), # USenglish, american
    ('en_gb', 'british'), # UKenglish
    ('en_ca', 'canadian'),
    ('en_au', 'australian'),
    ('en_nz', 'newzealand'),
    ('es_es', 'spanish'),
    ('fr_fr', 'french'), # francais
    ('fr_ca', 'canadien'),
    ('it_it', 'italian'),
    ('la_LA', 'latin'),
    ('pt_pt', 'portuguese'), # portuges
    ('pt_br', 'brazilian'), # brazil

    ## Remaining Babel language codes
    # ('??_??', 'afrikaans'),
    # ('??_??', 'bahasa'),
    # ('??_??', 'indonesian'),
    # ('??_??', 'indon'),
    # ('??_??', 'bahasai'),
    # ('??_??', 'bahasam'),
    # ('??_??', 'malay'),
    # ('??_??', 'melayu'),
    # ('??_??', 'basque'),
    # ('??_??', 'breton'),
    # ('??_??', 'bulgarian'),
    # ('??_??', 'catalan'),
    # ('??_??', 'croatian'),
    # ('??_??', 'czech'),
    # ('??_??', 'danish'),
    # ('??_??', 'dutch'),
    # ('??_??', 'estonian'),
    # ('??_??', 'finnish'),
    # ('??_??', 'acadian'),
    # ('??_??', 'galician'),
    # ('??_??', 'germanb'),
    # ('??_??', 'ngerman'),
    # ('??_??', 'naustrian'),
    # ('??_??', 'greek'),
    # ('??_??', 'polutonikogreek'),
    # ('??_??', 'hebrew'),
    # ('??_??', 'icelandic'),
    # ('??_??', 'interlingua'),
    # ('??_??', 'irish'),
    # ('??_??', 'lowersorbian'),
    # ('??_??', 'samin'),
    # ('??_??', 'norsk'),
    # ('??_??', 'nynorsk'),
    # ('??_??', 'polish'),
    # ('??_??', 'romanian'),
    # ('??_??', 'russian'),
    # ('??_??', 'scottish'),
    # ('??_??', 'slovak'),
    # ('??_??', 'slovene'),
    # ('??_??', 'swedish'),
    # ('??_??', 'serbian'),
    # ('??_??', 'turkish'),
    # ('??_??', 'ukrainian'),
    # ('??_??', 'uppersorbian'),
    # ('??_??', 'welsh'),
))

def lang2babel(lang):
    """Return the language used by babel, corresponding to the language code"""
    try:
        # Exact match
        if lang.lower() in BABEL_LANGUAGES:
            return BABEL_LANGUAGES[lang.lower()]
        # Only language code is provided (e.g. 'fr')
        for babel in BABEL_LANGUAGES:
            if babel.startswith(lang.lower()):
                return BABEL_LANGUAGES[babel]
        # A non existent country code is provided (e.g. 'fr_CD').
        language = lang.lower().split("_")[0]
        for babel in BABEL_LANGUAGES:
            if babel.startswith(language):
                LOGGER.error(
                    "Unknown country code '{}'. Using default '{}' instead.".format(
                        lang,
                        babel
                    )
                )
                return BABEL_LANGUAGES[babel]
    except KeyError:
        available = ", ".join(BABEL_LANGUAGES.keys())
        LOGGER.error(
            "Unknown language code '{}' (supported: {}). Using default 'english' instead.".format(
                lang,
                available
            )
        )
        return 'english'
