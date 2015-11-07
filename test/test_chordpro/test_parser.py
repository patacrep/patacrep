"""Tests for the chordpro parser."""

# pylint: disable=too-few-public-methods

import contextlib
import glob
import os
import unittest
from pkg_resources import resource_filename

from patacrep import files
from patacrep.build import DEFAULT_CONFIG
from patacrep.encoding import open_read

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

    @staticmethod
    @contextlib.contextmanager
    def chdir():
        """Context to temporarry change current directory to this file directory
        """
        olddir = os.getcwd()
        os.chdir(resource_filename(__name__, ""))
        yield
        os.chdir(olddir)

    def assertRender(self, destformat, sourcename, destname): # pylint: disable=invalid-name
        """Assert that `sourcename` is correctly rendered as `destname` in `destformat`.
        """
        with self.chdir():
            with open_read(destname) as expectfile:
                with disable_logging():
                    song = self.song_plugins[LANGUAGES[destformat]]['sgc'](sourcename, self.config)
                    self.assertMultiLineEqual(
                        song.render(output=sourcename).strip(),
                        expectfile.read().strip(),
                        )

    @classmethod
    def _iter_testmethods(cls):
        """Iterate over song files to test."""
        # Setting datadir
        cls.config = DEFAULT_CONFIG
        if 'datadir' not in cls.config:
            cls.config['datadir'] = []
        cls.config['datadir'].append('datadir')

        cls.song_plugins = files.load_plugins(
            datadirs=cls.config['datadir'],
            root_modules=['songs'],
            keyword='SONG_RENDERERS',
            )
        with cls.chdir():
            for source in sorted(glob.glob('*.source')):
                base = source[:-len(".source")]
                for dest in LANGUAGES:
                    destname = "{}.{}".format(base, dest)
                    if not os.path.exists(destname):
                        continue
                    yield (
                        "test_{}_{}".format(base, dest),
                        cls._create_test(base, dest),
                        )

    @classmethod
    def _create_test(cls, base, dest):
        """Return a function testing that `base` compilation in `dest` format.
        """

        def test_parse_render(self):
            """Test that `base` is correctly parsed and rendered."""
            if base is None or dest is None:
                return
            self.assertRender(dest, "{}.source".format(base), "{}.{}".format(base, dest))

        test_parse_render.__doc__ = (
            "Test that '{base}' is correctly parsed and rendererd into '{format}' format."
            ).format(base=os.path.basename(base), format=dest)
        return test_parse_render

    def test_clrf(self):
        """Test that source is correctly parsed and rendered when line endings are CRLF.
        """
        originalname = "newline.source"
        chordproname = "newline.crlf.source"
        with self.chdir():
            with open_read(originalname) as originalfile:
                with open(chordproname, 'w') as chordprofile:
                    for line in originalfile:
                        chordprofile.write(line.replace('\n', '\r\n'))
            for dest in LANGUAGES:
                with self.subTest(dest):
                    self.assertRender(dest, chordproname, "newline.{}".format(dest))
            os.remove(chordproname)
