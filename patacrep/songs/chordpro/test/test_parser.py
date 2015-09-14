"""Tests for the chordpro parser."""

# pylint: disable=too-few-public-methods

import glob
import os
import unittest

from patacrep.build import DEFAULT_CONFIG
from patacrep.songs.chordpro import ChordproSong
from patacrep.test import disable_logging

LANGUAGES = {
    'tex': 'latex',
    'sgc': 'chordpro',
}

# Set to True if you want to create missing rendered files
CREATE_MISSING_RENDERED_FILE = False

def load_tests(loader, tests, pattern):
    """
    Add all `*.source` files to the test suite.
    """
    del loader, tests, pattern
    suite = unittest.TestSuite()
    for source in sorted(glob.glob(os.path.join(
            os.path.dirname(__file__),
            '*.source',
        ))):
        single_test = TestSingleParsingRendering('run_test')
        setattr(single_test, 'filename', source)
        suite.addTest(single_test)
    return suite

class TestSingleParsingRendering(unittest.TestCase):
    """Test parsing and rendering"""

    maxDiff = None

    def run_test(self):
        """Test the self.filename (.source) file.

        For any given `foo.source`, it is parsed as a chordpro file, and
        should be rendered as `foo.sgc` with the chordpro renderer, and
        `foo.tex` with the latex renderer.
        """
        if not hasattr(self, 'filename'):
            return self.skipTest("No file to test")

        source = getattr(self, 'filename')
        config = DEFAULT_CONFIG.copy()
        config.update({
            'encoding': 'utf8',
            })
        base = source[:-len(".source")]
        for dest in LANGUAGES:
            destname = "{}.{}".format(base, dest)
            if not os.path.exists(destname):
                if CREATE_MISSING_RENDERED_FILE:
                    print("Creating " + destname)
                    with open(destname, 'w', encoding='utf8') as expectfile:
                        chordproname = "{}.source".format(base)
                        config['filename'] = chordproname
                        expectfile.write(
                            ChordproSong(None, chordproname, config).render(
                                output=chordproname,
                                output_format=LANGUAGES[dest],
                                )
                            )
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


