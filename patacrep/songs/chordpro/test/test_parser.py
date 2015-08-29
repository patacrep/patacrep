"""Tests for the chordpro parser."""

# pylint: disable=too-few-public-methods

import glob
import os
import unittest

from patacrep.build import DEFAULT_CONFIG
from patacrep.songs.chordpro import ChordproSong
from patacrep.test import disable_logging


class TestParsingRendering(unittest.TestCase):
    """Test parsing and rendering"""

    maxDiff = None

    def test_all(self):
        config = DEFAULT_CONFIG.copy()
        config.update({
            'encoding': 'utf8',
            })
        for source in sorted(glob.glob(os.path.join(
                os.path.dirname(__file__),
                '*.source',
            ))):
            base = source[:-len(".source")]
            with open("{}.sgc".format(base), 'r', encoding='utf8') as expectfile:
                chordproname = "{}.source".format(base)
                with disable_logging():
                    with self.subTest(base=os.path.basename(base)):
                        self.assertMultiLineEqual(
                            ChordproSong(None, chordproname, config).render(
                                output=chordproname,
                                output_format="chordpro",
                                ).strip(),
                            expectfile.read().replace(
                                "DIRNAME",
                                os.path.dirname(base),
                                ).strip(),
                            )
