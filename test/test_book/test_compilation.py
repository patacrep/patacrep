"""Tests for the songbook compilation."""

# pylint: disable=too-few-public-methods

import glob
import logging
import os
import sys
import subprocess
import unittest

import yaml

from patacrep.files import path2posix, chdir
from patacrep.songbook import prepare_songbook
from patacrep.build import SongbookBuilder
from patacrep import __DATADIR__

from .. import logging_reduced
from .. import dynamic # pylint: disable=unused-import

LOGGER = logging.getLogger(__name__)

class FileTest(unittest.TestCase, metaclass=dynamic.DynamicTest):
    """Test of songbook compilation.

    For any given `foo.yaml`, it performs several checks:
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
                '*.yaml',
            ))):
            base = os.path.splitext(songbook)[0]
            yield (
                "test_latex_generation_{}".format(os.path.basename(base)),
                cls._create_generation_test(base),
                )
            yield (
                "test_pdf_compilation_{}".format(os.path.basename(base)),
                cls._create_compilation_test(base),
                )
        for songbook in sorted(glob.glob(os.path.join(
                os.path.dirname(__file__),
                'onthefly',
                '*.yaml',
            ))):
            base = os.path.splitext(songbook)[0]
            yield (
                "test_latex_generation_onthefly_{}".format(os.path.basename(base)),
                cls._create_generation_test(base, True),
                )
            yield (
                "test_pdf_compilation_onthefly_{}".format(os.path.basename(base)),
                cls._create_compilation_test(base, True),
                )

    @classmethod
    def _create_generation_test(cls, base, onthefly=False):
        """Return a function testing that `base.tex` is correctly generated."""

        def test_generation(self):
            """Test that `base.tex` is correctly generated."""
            songbook = "{}.yaml".format(base)

            # Check tex generation
            if onthefly:
                self.compile_songbook_onthefly(base, ['tex'])
            else:
                self.assertEqual(0, self.compile_songbook(songbook, "tex"))

            # Check generated tex
            control = "{}.tex.control".format(base)
            if not os.path.exists(control):
                raise unittest.SkipTest('No control file for {}'.format(songbook))

            tex = "{}.tex".format(base)
            with open(control, mode="r", encoding="utf8") as expectfile:
                with open(tex, mode="r", encoding="utf8") as latexfile:
                    expected = expectfile.read().strip()
                    expected = expected.replace(
                        "@TEST_FOLDER@",
                        path2posix(os.path.dirname(__file__)),
                        )
                    expected = expected.replace(
                        "@LOCAL_DATA_FOLDER@",
                        path2posix(__DATADIR__),
                        )

                    expected = expected.replace(
                        "@DATA_FOLDER@",
                        path2posix(
                            subprocess.check_output(
                                [sys.executable, "-c", 'import patacrep; print(patacrep.__DATADIR__)'], # pylint: disable=line-too-long
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
    def _create_compilation_test(cls, base, onthefly=False):
        """Return a function testing that `base.tex` is correctly compiled."""
        @unittest.skipIf('APPVEYOR' in os.environ,
                         "AppVeyor does not support lualatex compilation yet")
        def test_compilation(self):
            """Test that `base` is rendered to pdf."""
            # Check compilation
            songbook = "{}.yaml".format(base)
            if onthefly:
                self.compile_songbook_onthefly(base)
            else:
                self.assertEqual(0, self.compile_songbook(songbook))

        test_compilation.__doc__ = (
            "Test that '{base}' is correctly compiled."
            ).format(base=os.path.basename(base))
        return test_compilation

    @staticmethod
    def compile_songbook(songbook, steps=None):
        """Compile songbook, and return the command return code."""
        command = [sys.executable, '-m', 'patacrep.songbook', '--cache=no', songbook]
        if steps:
            command.extend(['--steps', steps])

        # Continuous Integration will be verbose
        if 'CI' in os.environ:
            command.append('-v')

        try:
            subprocess.check_call(
                command,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=os.path.dirname(songbook),
                )
            return 0
        except subprocess.CalledProcessError as error:
            LOGGER.warning(error.output)
            return error.returncode

    @staticmethod
    def compile_songbook_onthefly(base, steps=None):
        """Compile songbook "on the fly": without a physical songbook file."""

        with open(base + ".yaml", mode="r", encoding="utf8") as sbfile:
            sbyaml = yaml.safe_load(sbfile)

        outputdir = os.path.dirname(base)
        outputname = os.path.basename(base)
        datadir_prefix = os.path.join(outputdir, '..')
        songbook = prepare_songbook(sbyaml, outputdir, outputname, datadir_prefix=datadir_prefix)
        songbook['_error'] = "fix"
        songbook['_cache'] = True

        sb_builder = SongbookBuilder(songbook)
        sb_builder.unsafe = True

        with chdir(outputdir):
            # Continuous Integration will be verbose
            if 'CI' in os.environ:
                with logging_reduced(level=logging.DEBUG):
                    sb_builder.build_steps(steps)
            else:
                sb_builder.build_steps(steps)
