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

class FileTestMeta(type):
    """Metaclass that creates on-the-fly test function according to files.

    See the :class:`FileTest` documentation for more information.
    """

    def __init__(cls, name, bases, nmspc):
        super().__init__(name, bases, nmspc)

        for source in sorted(glob.glob(os.path.join(
                os.path.dirname(__file__),
                '*.source',
            ))):
            base = source[:-len(".source")]
            for dest in LANGUAGES:
                destname = "{}.{}".format(base, dest)
                if not os.path.exists(destname):
                    continue
                setattr(
                    cls,
                    "test_{}_{}".format(os.path.basename(base), dest),
                    cls._create_test(base, dest),
                    )

    @staticmethod
    def _create_test(base, dest):
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
                        ChordproSong(None, chordproname, DEFAULT_CONFIG).render(
                            output=chordproname,
                            output_format=LANGUAGES[dest],
                            ).strip(),
                        expectfile.read().strip(),
                        )

        test_parse_render.__doc__ = (
            "Test that '{base}' is correctly parsed and rendererd into '{format}' format."
            ).format(base=os.path.basename(base), format=dest)
        return test_parse_render

class FileTest(unittest.TestCase, metaclass=FileTestMeta):
    """Test of chorpro parser, and several renderers.

    For any given `foo.source`, it is parsed as a chordpro file, and should be
    rendered as `foo.sgc` with the chordpro renderer, and `foo.tex` with the
    latex renderer.

    This class does nothing by itself, but its metaclass populates it with test
    methods testing parser and renderers.
    """

    maxDiff = None
