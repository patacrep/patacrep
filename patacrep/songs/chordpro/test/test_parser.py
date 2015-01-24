"""Tests for the chordpro parser."""

# pylint: disable=too-few-public-methods

import glob
import os
import unittest

from patacrep.songs.chordpro import syntax as chordpro

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
        with open("{}.sgc".format(self.basename), 'r', encoding='utf8') as sourcefile:
            with open("{}.txt".format(self.basename), 'r', encoding='utf8') as expectfile:
                #print(os.path.basename(sourcefile.name))
                #with open("{}.txt.diff".format(self.basename), 'w', encoding='utf8') as difffile:
                #    difffile.write(
                #        str(chordpro.parse_song(
                #            sourcefile.read(),
                #            os.path.basename(sourcefile.name),
                #            )).strip()
                #        )
                #    sourcefile.seek(0)
                self.assertMultiLineEqual(
                    str(chordpro.parse_song(
                        sourcefile.read(),
                        os.path.abspath(sourcefile.name),
                        )).strip(),
                    expectfile.read().strip().replace("DIRNAME", os.path.dirname(self.basename)),
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
