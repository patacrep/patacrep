"""Tests for the chordpro parser."""

# pylint: disable=too-few-public-methods

import contextlib
import glob
import os
import unittest
from pkg_resources import resource_filename

from patacrep import files, __DATADIR__
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

    @classmethod
    def setUpClass(cls):
        cls._overwrite_clrf()

    @classmethod
    def tearDownClass(cls):
        cls._reset_clrf()

    @staticmethod
    @contextlib.contextmanager
    def chdir():
        """Context to temporarry change current directory to this file directory
        """
        with files.chdir(resource_filename(__name__, "")):
            yield

    def assertRender(self, base, destformat): # pylint: disable=invalid-name
        """Assert that `{base}.source` is correctly rendered in the `destformat`.
        """
        sourcename = "{}.source".format(base)
        destname = "{}.{}".format(base, destformat)
        with self.chdir():
            with open_read(destname) as expectfile:
                with disable_logging():
                    song = self.song_plugins[LANGUAGES[destformat]]['sgc'](sourcename, self.config)
                    self.assertMultiLineEqual(
                        song.render().strip(),
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
        cls.config['datadir'].append(__DATADIR__)

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

            with files.chdir('errors'):
                for source in sorted(glob.glob('*.source')):
                    base = source[:-len(".source")]
                    yield (
                        "test_{}_failure".format(base),
                        cls._create_failure(base),
                        )

    @classmethod
    def _create_test(cls, base, dest):
        """Return a function testing that `base` compilation in `dest` format.
        """
        test_parse_render = lambda self: self.assertRender(base, dest)
        test_parse_render.__doc__ = (
            "Test that '{base}' is correctly parsed and rendererd into '{format}' format."
            ).format(base=os.path.basename(base), format=dest)
        return test_parse_render

    @classmethod
    def _create_failure(cls, base):
        """Return a function testing that `base` parsing fails.
        """

        def test_parse_failure(self):
            """Test that `base` parsing fails."""
            sourcename = "{}.source".format(base)
            with self.chdir():
                with files.chdir('errors'):
                    parser = self.song_plugins[LANGUAGES['sgc']]['sgc']
                    self.assertRaises(SyntaxError, parser, sourcename, self.config)

        test_parse_failure.__doc__ = (
            "Test that '{base}' parsing fails."
            ).format(base=os.path.basename(base))
        return test_parse_failure

    @classmethod
    def _overwrite_clrf(cls):
        """Overwrite `*.crlf.source` files to force the CRLF line endings.
        """
        with cls.chdir():
            for crlfname in sorted(glob.glob('*.crlf.source')):
                base = crlfname[:-len(".crlf.source")]
                sourcename = base + ".source"
                with open_read(sourcename) as sourcefile:
                    with open(crlfname, 'w') as crlffile:
                        for line in sourcefile:
                            crlffile.write(line.replace('\n', '\r\n'))

    @classmethod
    def _reset_clrf(cls):
        """Reset `*.crlf.source` files.
        """
        crlf_msg = """# This content will be overwritten with `{}.source` content
# with windows line endings (CRLF) - for testing purposes
"""
        with cls.chdir():
            for crlfname in sorted(glob.glob('*.crlf.source')):
                base = crlfname[:-len(".crlf.source")]
                with open(crlfname, 'w') as crlffile:
                    crlffile.write(crlf_msg.format(base))
