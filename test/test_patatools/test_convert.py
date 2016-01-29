"""Tests of the patatools-convert command."""

# pylint: disable=too-few-public-methods

import contextlib
import glob
import os
import unittest

from pkg_resources import resource_filename

from patacrep import files
from patacrep.tools.__main__ import main as tools_main
from patacrep.encoding import open_read
from patacrep.tools.convert.__main__ import main as convert_main

from .. import dynamic # pylint: disable=unused-import
from .. import logging_reduced

class TestConvert(unittest.TestCase, metaclass=dynamic.DynamicTest):
    """Test of the "patatools convert" subcommand"""

    @staticmethod
    def _system(main, args):
        try:
            main(args)
        except SystemExit as systemexit:
            return systemexit.code
        return 0

    def assertConvert(self, basename, in_format, out_format): # pylint: disable=invalid-name
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
                            self.assertEqual(
                                self._system(main, args + [in_format, out_format, sourcename]),
                                0,
                                )
                            expected = controlfile.read().strip().replace(
                                "@TEST_FOLDER@",
                                files.path2posix(resource_filename(__name__, "")),
                                )
                            with open_read(destname) as destfile:
                                self.assertMultiLineEqual(
                                    destfile.read().replace('\r\n', '\n').strip(),
                                    expected.strip(),
                                    )

    def assertFailConvert(self, basename, in_format, out_format): # pylint: disable=invalid-name
        """Test of the "patatools convert" subcommand"""
        sourcename = "{}.{}".format(basename, in_format)
        destname = "{}.{}".format(basename, out_format)
        for main, args in [
                (tools_main, ["patatools", "convert"]),
                (convert_main, ["patatools-convert"]),
            ]:
            with self.subTest(main=main, args=args):
                with self.chdir("test_convert_failure"):
                    with logging_reduced():
                        if os.path.exists(destname):
                            os.remove(destname)
                        self.assertEqual(
                            self._system(main, args + [in_format, out_format, sourcename]),
                            1,
                            )

    @staticmethod
    @contextlib.contextmanager
    def chdir(*pathlist):
        """Temporary change current directory, relative to this file directory"""
        with files.chdir(resource_filename(__name__, ""), *pathlist):
            yield

    @classmethod
    def _iter_testmethods(cls):
        """Iterate over song files to test."""
        for directory, create_test in [
                ("test_convert_success", cls._create_test_success),
                ("test_convert_failure", cls._create_test_failure),
            ]:
            with cls.chdir(directory):
                for control in sorted(glob.glob('*.*.*.control')):
                    [*base, in_format, out_format, _] = control.split('.')
                    base = '.'.join(base)
                    yield (
                        "test_{}_{}_{}".format(base, in_format, out_format),
                        create_test(base, in_format, out_format),
                        )

    @classmethod
    def _create_test_success(cls, base, in_format, out_format):
        """Return a function testing conversion.

        :param str base: Base name of the file to convert.
        :param str in_format: Source format.
        :param str out_format: Destination format.
        """
        test_parse_render = lambda self: self.assertConvert(base, in_format, out_format)
        test_parse_render.__doc__ = (
            "Test that '{base}.{in_format}' is correctly converted to '{out_format}'."
            ).format(base=os.path.basename(base), in_format=in_format, out_format=out_format)
        return test_parse_render

    @classmethod
    def _create_test_failure(cls, base, in_format, out_format):
        """Return a function testing failing conversions
        """
        test_parse_render = lambda self: self.assertFailConvert(base, in_format, out_format)
        test_parse_render.__doc__ = (
            "Test that '{base}.{in_format}' raises an error when trying to convert it to '{out_format}'." # pylint: disable=line-too-long
            ).format(base=os.path.basename(base), in_format=in_format, out_format=out_format)
        return test_parse_render
