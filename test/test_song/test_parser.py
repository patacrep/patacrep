"""Tests for the chordpro parser."""

# pylint: disable=too-few-public-methods

import contextlib
import glob
import os
import unittest
from pkg_resources import resource_filename

from patacrep import files
from patacrep.encoding import open_read
from patacrep.build import config_model
from patacrep.songs import errors

from .. import logging_reduced
from .. import dynamic # pylint: disable=unused-import

OUTPUTS = {
    'csg': ['csg', 'tsg', 'html'],
    'tsg': ['tsg'],
}

class FileTest(unittest.TestCase, metaclass=dynamic.DynamicTest):
    """Test of chorpro parser, and several renderers.

    For any given `foo.input_format.source`, the file is parsed as `input_format` and
    rendered as many times as a `foo.out_format` exists (if `out_format` is a supported
    output format).

    For instance `foo.csg.source` (chordpro song) will be rendered as LaTeX, if a file
    `foo.tsg` exitsts. The result of the rendering will be compared with the `foo.tsg` file.

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
    def chdir(*path):
        """Temporary change current directory, relative to this file directory"""
        with files.chdir(resource_filename(__name__, ""), *path):
            yield

    def assertRender(self, base, in_format, out_format): # pylint: disable=invalid-name
        """Assert that `{base}.{in_format}.source` is correctly rendered in the `out_format`.
        """
        sourcename = "{}.{}.source".format(base, in_format)
        destname = "{}.{}".format(base, out_format)
        with self.chdir():
            with open_read(destname) as expectfile:
                with logging_reduced():
                    song = self.song_plugins[out_format][in_format](sourcename, self.config)
                    expected = expectfile.read().strip().replace(
                        "@TEST_FOLDER@",
                        files.path2posix(resource_filename(__name__, "")),
                        )
                    self.assertMultiLineEqual(
                        song.render().strip(),
                        expected,
                        )

    @classmethod
    def _iter_testmethods(cls):
        """Iterate over song files to test."""
        # Setting datadir
        # Load the default songbook config
        cls.config = config_model('default')['en']

        if '_datadir' not in cls.config:
            cls.config['_datadir'] = []
        cls.config['_datadir'].append('datadir')

        cls.song_plugins = files.load_plugins(
            datadirs=cls.config['_datadir'],
            root_modules=['songs'],
            keyword='SONG_RENDERERS',
            )
        with cls.chdir():
            for source in sorted(glob.glob('*.*.source')):
                [*base, in_format, _] = source.split('.')
                base = '.'.join(base)
                for out_format in OUTPUTS[in_format]:
                    outname = "{}.{}".format(base, out_format)
                    if not os.path.exists(outname):
                        continue
                    yield (
                        "test_{}_{}_2_{}".format(base, in_format, out_format),
                        cls._create_test(base, in_format, out_format),
                        )

            if os.path.isdir("errors"):
                with cls.chdir('errors'):
                    for source in sorted(glob.glob('*.*.source')):
                        [*base, in_format, _] = source.split('.')
                        base = '.'.join(base)
                        yield (
                            "test_{}_{}_failure".format(base, in_format),
                            cls._create_failure(base, in_format),
                            )

    @classmethod
    def _create_test(cls, base, in_format, out_format):
        """Return a function testing that `base` compilation in `out_format` format.
        """
        test_parse_render = lambda self: self.assertRender(base, in_format, out_format)
        test_parse_render.__doc__ = (
            "Test that '{base}.{in_format}' is correctly parsed and rendererd into '{out_format}'."
            ).format(base=os.path.basename(base), in_format=in_format, out_format=out_format)
        return test_parse_render

    @classmethod
    def _create_failure(cls, base, in_format, out_format='tsg'):
        """Return a function testing that `base` parsing fails.
        """

        def test_parse_failure(self):
            """Test that `base` parsing fails."""
            sourcename = "{}.{}.source".format(base, in_format)
            with self.chdir('errors'):
                parser = self.song_plugins[out_format][in_format]
                self.assertRaises(errors.SongSyntaxError, parser, sourcename, self.config)

        test_parse_failure.__doc__ = (
            "Test that '{base}' parsing fails."
            ).format(base=os.path.basename(base))
        return test_parse_failure

    @classmethod
    def _overwrite_clrf(cls):
        """Overwrite `*.crlf.source` files to force the CRLF line endings.
        """
        with cls.chdir():
            for crlfname in sorted(glob.glob('*.crlf.*.source')):
                [*base, _, in_format, source] = crlfname.split('.')
                sourcename = '.'.join(base + [in_format, source])
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
            for crlfname in sorted(glob.glob('*.crlf.*.source')):
                [*base, _crlf, in_format, _] = crlfname.split('.')
                base = '.'.join(base + [in_format])
                with open(crlfname, 'w') as crlffile:
                    crlffile.write(crlf_msg.format(base))
