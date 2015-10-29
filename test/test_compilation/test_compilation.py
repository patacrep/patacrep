"""Tests for the chordpro parser."""

# pylint: disable=too-few-public-methods

import glob
import os
import sys
import subprocess
import unittest
import logging

from patacrep.encoding import open_read

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
                    expected = expectfile.read().strip()
                    expected = expected.replace(
                        "@TEST_FOLDER@",
                        os.path.dirname(__file__),
                        )

                    expected = expected.replace(
                        "@DATA_FOLDER@",
                        subprocess.check_output(
                            [sys.executable, "-c", 'import patacrep, pkg_resources; print(pkg_resources.resource_filename(patacrep.__name__, "data"))'], # pylint: disable=line-too-long
                            universal_newlines=True,
                            cwd=os.path.dirname(songbook),
                            ).strip(),
                        )

                    self.assertMultiLineEqual(
                        latexfile.read().strip(),
                        expected,
                        )

            # Check compilation
            if 'TRAVIS' not in os.environ:
                # Travis does not support lualatex compilation yet
                self.assertEqual(0, self.compile_songbook(songbook))

        test_compile.__doc__ = (
            "Test that '{base}' is correctly compiled."
            ).format(base=os.path.basename(base))
        return test_compile

    @staticmethod
    def compile_songbook(songbook, steps=None):
        """Compile songbook, and return the command return code."""
        command = [sys.executable, '-m', 'patacrep.songbook', songbook, '-v']
        if steps:
            command.extend(['--steps', steps])

        current_env = os.environ.copy()
        #current_env['PYTHONPATH'] = ':'.join(sys.path)
        print("#######")
        print(command)
        print("#######")

        print("## sys.path (internal)")
        print(sys.path)

        print("## sys.path (external)")
        syspath = subprocess.check_output([sys.executable, "-c", 'import sys;print(sys.path)'],
                stderr=subprocess.STDOUT,
                cwd=os.path.dirname(songbook),
                env=current_env)
        print(syspath)

        print("## import (external)")
        extimport = subprocess.check_output([sys.executable, "-c", 'import patacrep.songbook as sb;print(sb)'])
        print(extimport)

        print("### empty module")
        try:
            emptymod = subprocess.check_output([sys.executable, "-m", 'patacrep.songbook', 'empty.sb'],
                stderr=subprocess.STDOUT)
            print(emptymod)
        except subprocess.CalledProcessError as error:
            print(error.output)

        print("### cwd module")
        try:
            emptymod = subprocess.check_output(
                [sys.executable, "-m", 'patacrep.songbook', 'cwd.sb'],
                stderr=subprocess.STDOUT,
                cwd=os.path.dirname(songbook),
                env=current_env
                )
            print(emptymod)
        except subprocess.CalledProcessError as error:
            print(error.output)

        print("### import cwd")
        try:
            importcwd = subprocess.check_output(
                [sys.executable, "-c", 'import patacrep.songbook as sb;print(sb)'],
                stderr=subprocess.STDOUT,
                cwd=os.path.dirname(songbook),
                env=current_env
                )
            print(importcwd)
        except subprocess.CalledProcessError as error:
            print(error.output)

        print("### dir site-packages")
        dirres = subprocess.check_output(["dir", 'C:\projects\patacrep\.tox\py34\lib\site-packages'])
        print(dirres)


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
