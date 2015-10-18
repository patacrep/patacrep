"""Tests for the chordpro parser."""

# pylint: disable=too-few-public-methods

import glob
import os
import unittest

from patacrep.build import DEFAULT_CONFIG
from patacrep.songs.chordpro import ChordproSong

from .. import disable_logging
from .. import dynamic # pylint: disable=unused-import

LANGUAGES = {
    'tex': 'latex',
    'sgc': 'chordpro',
    'html': 'html',
}

class FileTest(unittest.TestCase, metaclass=dynamic.DynamicTest):
    """Test of chorpro parser, and several renderers.

    For any given `foo.source`, it is parsed as a chordpro file, and should be
    rendered as `foo.sgc` with the chordpro renderer, and `foo.tex` with the
    latex renderer.

    This class does nothing by itself, but its metaclass populates it with test
    methods testing parser and renderers.
    """

    maxDiff = None

    @classmethod
    def _iter_testmethods(cls):
        """Iterate over song files to test."""
        for source in sorted(glob.glob(os.path.join(
                os.path.dirname(__file__),
                '*.source',
            ))):
            base = source[:-len(".source")]
            for dest in LANGUAGES:
                destname = "{}.{}".format(base, dest)
                if not os.path.exists(destname):
                    continue
                yield (
                    "test_{}_{}".format(os.path.basename(base), dest),
                    [base, dest],
                    )

    @classmethod
    def _create_test(cls, base, dest):
        """Return a function testing that `base` compilation in `dest` format.
        """

        def test_parse_render(self):
            """Test that `base` is correctly parsed and rendered."""
            if base is None or dest is None:
                return
            destname = "{}.{}".format(base, dest)
            with open(destname, 'r', encoding='utf8') as expectfile:
                chordproname = "{}.source".format(base)
                with disable_logging():
                    self.assertMultiLineEqual(
                        ChordproSong(chordproname, DEFAULT_CONFIG).render(
                            output=chordproname,
                            output_format=LANGUAGES[dest],
                            ).strip(),
                        expectfile.read().strip(),
                        )

        test_parse_render.__doc__ = (
            "Test that '{base}' is correctly parsed and rendererd into '{format}' format."
            ).format(base=os.path.basename(base), format=dest)
        return test_parse_render

