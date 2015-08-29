"""Tests for the chordpro parser."""

# pylint: disable=too-few-public-methods

import glob
import os
import unittest

from patacrep.build import DEFAULT_CONFIG
from patacrep.songs.chordpro import ChordproSong
from patacrep.test import disable_logging


class ParserTxtRenderer(unittest.TestCase):
    """Test parser, and renderer as a txt file."""

    maxDiff = None

    def __init__(self, methodname="runTest", basename=None):
        super().__init__(methodname)
        self.basename = basename

    def shortDescription(self):
        return "Parsing file '{}.txt'.".format(self.basename)

    def runTest(self):
        """Test txt output (default, debug output)."""
        # pylint: disable=invalid-name

        if self.basename is None:
            return
        config = DEFAULT_CONFIG.copy()
        config.update({
            'encoding': 'utf8',
            '_compiled_authwords': {},
            })
        with open("{}.txt".format(self.basename), 'r', encoding='utf8') as expectfile:
            chordproname = "{}.sgc".format(self.basename)
            with disable_logging():
                self.assertMultiLineEqual(
                    ChordproSong(None, chordproname, config).render(
                        output=chordproname,
                        output_format="chordpro",
                        ).strip(),
                    expectfile.read().replace(
                        "DIRNAME",
                        os.path.dirname(self.basename),
                        ).strip(),
                    )

def load_tests(__loader, tests, __pattern):
    """Load several tests given test files present in the directory."""
    # Load all txt files as tests
    for txt in sorted(glob.glob(os.path.join(
            os.path.dirname(__file__),
            '*.txt',
        ))):
        tests.addTest(ParserTxtRenderer(basename=txt[:-len('.txt')]))
    return tests
