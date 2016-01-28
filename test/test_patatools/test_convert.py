"""Tests of the patatools-convert command."""

# pylint: disable=too-few-public-methods

from pkg_resources import resource_filename
import contextlib
import glob
import os
import shutil
import unittest

from patacrep import files
from patacrep.tools.__main__ import main as tools_main
from patacrep.encoding import open_read
from patacrep.tools.convert.__main__ import main as convert_main
from patacrep.songbook.__main__ import main as songbook_main

from .. import dynamic
from .. import logging_reduced

class TestConvert(unittest.TestCase, metaclass=dynamic.DynamicTest):
    """Test of the "patatools convert" subcommand"""

    def _system(self, main, args):
        try:
            main(args)
        except SystemExit as systemexit:
            return systemexit.code
        return 0

    def assertConvert(self, basename, in_format, out_format):
        """Test of the "patatools convert" subcommand"""
        sourcename = "{}.{}".format(basename, in_format)
        destname = "{}.{}".format(basename, out_format)
        controlname = "{}.{}.control".format(sourcename, out_format)
        for main, args in [
                (tools_main, ["patatools", "convert"]),
                (convert_main, ["patatools-convert"]),
            ]:
            with self.subTest(main=main, args=args):
                with self.chdir("test_convert_success"):
                    with open_read(controlname) as controlfile:
                        with logging_reduced():
                            if os.path.exists(destname):
                                os.remove(destname)
                            self._system(main, args + [in_format, out_format, sourcename])
                            expected = controlfile.read().strip().replace(
                                "@TEST_FOLDER@",
                                files.path2posix(resource_filename(__name__, "")),
                                )
                            with open_read(destname) as destfile:
                                self.assertMultiLineEqual(
                                    destfile.read().strip(),
                                    expected,
                                    )

    @staticmethod
    @contextlib.contextmanager
    def chdir(*path):
        """Context to temporarry change current directory, relative to this file directory
        """
        with files.chdir(resource_filename(__name__, ""), *path):
            yield

    @classmethod
    def _iter_testmethods(cls):
        """Iterate over song files to test."""
        with cls.chdir("test_convert_success"):
            for control in sorted(glob.glob('*.*.*.control')):
                [*base, in_format, out_format, _] = control.split('.')
                base = '.'.join(base)
                yield (
                    "test_{}_{}_{}".format(base, in_format, out_format),
                    cls._create_test(base, in_format, out_format),
                    )

    @classmethod
    def _create_test(cls, base, in_format, out_format):
        """Return a function testing that `base` compilation from `in_format` to `out_format` format.
        """
        test_parse_render = lambda self: self.assertConvert(base, in_format, out_format)
        test_parse_render.__doc__ = (
            "Test that '{base}.{in_format}' is correctly converted to '{out_format}'."
            ).format(base=os.path.basename(base), in_format=in_format, out_format=out_format)
        return test_parse_render
