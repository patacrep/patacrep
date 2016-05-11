"""Dumb and very very incomplete LaTeX parser.

This module uses an LALR parser to try to parse LaTeX code. LaTeX language
*cannot* be parsed by an LALR parser, so this is a very simple attemps, which
will work on simple cases, but not on complex ones.
"""

import logging
from collections import OrderedDict

from patacrep import errors
from patacrep.latex.syntax import tex2plain, parse_song

LOGGER = logging.getLogger(__name__)

DEFAULT_LANGUAGE = "en_us"

BABEL_LANGUAGES = OrderedDict((
    ('de_de', 'ngerman'), # german (old), germanb (like german)
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

class UnknownLanguage(errors.SharedError):
    """Error: Unknown language."""

    def __init__(self, *, original, fallback, message):
        super().__init__()
        self.original = original
        self.fallback = fallback
        self.message = message

    @property
    def babel(self):
        """Return the fallback babel language."""
        return BABEL_LANGUAGES[self.fallback]

    def __str__(self):
        return self.message

    @property
    def __dict__(self):
        parent = vars(super())
        parent.update({
            'fallback': self.fallback,
            'original': self.original,
            })
        return parent

def checklanguage(lang):
    """Check that `lang` is a known language.

    Raise an :class:`UnknownLanguage` exception if not.
    """
    # Exact match
    if lang.lower() in BABEL_LANGUAGES:
        return lang.lower()
    # Only language code is provided (e.g. 'fr')
    for babel in BABEL_LANGUAGES:
        if babel.startswith(lang.lower()):
            return babel
    # A non existent country code is provided (e.g. 'fr_CD').
    language = lang.lower().split("_")[0]
    for babel in BABEL_LANGUAGES:
        if babel.startswith(language):
            raise UnknownLanguage(
                original=lang,
                fallback=babel,
                message="Unknown country code '{}'. Using default '{}' instead.".format(
                    lang,
                    babel
                )
            )
    # Error: no (exact or approximate) match found
    available = ", ".join(BABEL_LANGUAGES.keys())
    raise UnknownLanguage(
        original=lang,
        fallback=DEFAULT_LANGUAGE,
        message=(
            "Unknown language code '{}' (supported: {}). Using "
            "default '{}' instead."
            ).format(
                lang,
                available,
                DEFAULT_LANGUAGE,
            )
    )

def lang2babel(lang):
    """Return the language used by babel, corresponding to the language code

    Raises an `UnknownLanguage` exception if the `lang` argument is not known,
    the :attr:`fallback` attribute of the exception being the existing
    alternative language that can be used instead.
    """
    return BABEL_LANGUAGES[checklanguage(lang)]
