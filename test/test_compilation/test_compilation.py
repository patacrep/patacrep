"""Tests for the chordpro parser."""

# pylint: disable=too-few-public-methods

import glob
import logging
import os
import subprocess
import unittest

from patacrep.encoding import open_read
from patacrep.files import path2posix

from .. import dynamic # pylint: disable=unused-import

LOGGER = logging.getLogger(__name__)

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
        """Iterate over dynamically generated test methods."""
        for songbook in sorted(glob.glob(os.path.join(
                os.path.dirname(__file__),
                '*.sb',
            ))):
            base = songbook[:-len(".sb")]
            control = "{}.tex.control".format(base)
            if not os.path.exists(control):
                continue
            yield (
                "test_generation_{}".format(os.path.basename(base)),
                cls._create_generation_test(base),
                )
            yield (
                "test_compilation_{}".format(os.path.basename(base)),
                cls._create_compilation_test(base),
                )

    @classmethod
    def _create_generation_test(cls, base):
        """Return a function testing that `base.tex` is correctly generated."""

        def test_generation(self):
            """Test that `base.tex` is correctly generated."""
            songbook = "{}.sb".format(base)

            # Check tex generation
            self.assertEqual(0, self.compile_songbook(songbook, "tex"))

            # Check generated tex
            control = "{}.tex.control".format(base)
            tex = "{}.tex".format(base)
            with open_read(control) as expectfile:
                with open_read(tex) as latexfile:
                    expected = expectfile.read().strip()
                    expected = expected.replace(
                        "@TEST_FOLDER@",
                        path2posix(os.path.dirname(__file__)),
                        )

                    expected = expected.replace(
                        "@DATA_FOLDER@",
                        path2posix(
                            subprocess.check_output(
                                ["python", "-c", 'import patacrep, pkg_resources; print(pkg_resources.resource_filename(patacrep.__name__, "data"))'], # pylint: disable=line-too-long
                                universal_newlines=True,
                                cwd=os.path.dirname(songbook),
                                ).strip()
                        ),
                        )

                    self.assertMultiLineEqual(
                        latexfile.read().strip(),
                        expected,
                        )

        test_generation.__doc__ = (
            "Test that '{base}' is correctly generated."
            ).format(base=os.path.basename(base))
        return test_generation

    @classmethod
    def _create_compilation_test(cls, base):
        """Return a function testing that `base.tex` is correctly compiled."""
        @unittest.skipIf('TRAVIS' in os.environ,
                         "Travis does not support lualatex compilation yet")
        def test_compilation(self):
            """Test that `base` is rendered to pdf."""
            # Check compilation
            songbook = "{}.sb".format(base)
            self.assertEqual(0, self.compile_songbook(songbook))

        test_compilation.__doc__ = (
            "Test that '{base}' is correctly compiled."
            ).format(base=os.path.basename(base))
        return test_compilation

    @staticmethod
    def compile_songbook(songbook, steps=None):
        """Compile songbook, and return the command return code."""
        command = ['python', '-m', 'patacrep.songbook', songbook, '-v']
        if steps:
            command.extend(['--steps', steps])

        try:
            subprocess.check_output(
                command,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=os.path.dirname(songbook),
                )
            return 0
        except subprocess.CalledProcessError as error:
            LOGGER.warning(error.output)
            return error.returncode
