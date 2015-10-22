"""Tests for the chordpro parser."""

# pylint: disable=too-few-public-methods

import glob
import os
import subprocess
import unittest

from patacrep.encoding import open_read
from pkg_resources import resource_filename

from .. import dynamic # pylint: disable=unused-import


class FileTest(unittest.TestCase, metaclass=dynamic.DynamicTest):
    """Test of songbook compilation.

    For any given `foo.sb`, it performs several checks:
    - the corresponding tex file is generated;
    - the generated tex file matches the `foo.tex.control` control file;
    - the compilation (tex, pdf, indexes) works without errors.

    This class does nothing by itself, but its metaclass populates it with test
    methods testing parser and renderers.
    """

    maxDiff = None

    @classmethod
    def _iter_testmethods(cls):
        """Iterate over songbook files to test."""
        for songbook in sorted(glob.glob(os.path.join(
                os.path.dirname(__file__),
                '*.sb',
            ))):
            base = songbook[:-len(".sb")]
            control = "{}.tex.control".format(base)
            if not os.path.exists(control):
                continue
            yield (
                "test_{}".format(os.path.basename(base)),
                [base],
                )

    @classmethod
    def _create_test(cls, base):
        """Return a function testing that `base` compiles."""

        def test_compile(self):
            """Test that `base` is correctly compiled."""
            if base is None:
                return

            songbook = "{}.sb".format(base)

            # Check tex generation
            self.assertEqual(0, self.compile_songbook(songbook, "tex"))

            # Check generated tex
            control = "{}.tex.control".format(base)
            tex = "{}.tex".format(base)
            with open_read(control) as expectfile:
                with open_read(tex) as latexfile:
                    self.assertMultiLineEqual(
                        latexfile.read().strip(),
                        expectfile.read().strip(),
                        )

            # Check compilation
            self.assertEqual(0, self.compile_songbook(songbook))

        test_compile.__doc__ = (
            "Test that '{base}' is correctly compiled."
            ).format(base=os.path.basename(base))
        return test_compile

    @staticmethod
    def compile_songbook(songbook, steps=None):
        """Compile songbook, and return the command return code."""
        command = ['python', '-m', 'patacrep.songbook', songbook]
        if steps:
            command.extend(['--steps', steps])

        return subprocess.check_call(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=os.path.dirname(songbook),
            )

    def assertMultiLineEqual(self, result, expected, msg=None):
        """Replace the placeholder paths with the local paths"""

        placeholder = "@TEST_FOLDER@"
        localpath = os.path.dirname(__file__)
        expected = expected.replace(placeholder, localpath)

        import patacrep
        placeholder = "@PACKAGE_FOLDER@"
        localpath = os.path.abspath(resource_filename(patacrep.__name__, ''))
        expected = expected.replace(placeholder, localpath)

        return super().assertMultiLineEqual(result, expected, msg)
