"""Tests for the chordpro parser."""

# pylint: disable=too-few-public-methods

import glob
import os
import unittest

from patacrep.build import DEFAULT_CONFIG
from patacrep.songs.chordpro import ChordproSong

from .. import disable_logging

LANGUAGES = {
    'tex': 'latex',
    'sgc': 'chordpro',
}

class TestParsingRendering(unittest.TestCase):
    """Test parsing and rendering"""

    maxDiff = None

    def test_all(self):
        """Test of chorpro parser, and several renderers.

        For any given `foo.source`, it is parsed as a chordpro file, and
        should be rendered as `foo.sgc` with the chordpro renderer, and
        `foo.tex` with the latex renderer.
        """
        config = DEFAULT_CONFIG.copy()
        config.update({
            'encoding': 'utf8',
            })
        for source in sorted(glob.glob(os.path.join(
                os.path.dirname(__file__),
                '*.source',
            ))):
            base = source[:-len(".source")]
            for dest in LANGUAGES:
                destname = "{}.{}".format(base, dest)
                if not os.path.exists(destname):
                    continue
                with open(destname, 'r', encoding='utf8') as expectfile:
                    chordproname = "{}.source".format(base)
                    config['filename'] = chordproname
                    with disable_logging():
                        with self.subTest(base=os.path.basename(base), format=dest):
                            self.assertMultiLineEqual(
                                ChordproSong(None, chordproname, config).render(
                                    output=chordproname,
                                    output_format=LANGUAGES[dest],
                                    ).strip(),
                                expectfile.read().strip(),
                                )
