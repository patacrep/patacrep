"""Tests for the chordpro parser."""

# pylint: disable=too-few-public-methods

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

    @classmethod
    def _iter_testmethods(cls):
        """Iterate over song files to test."""
        # Setting datadir
        cls.config = DEFAULT_CONFIG
        if 'datadir' not in cls.config:
            cls.config['datadir'] = []
        cls.config['datadir'].append(resource_filename(__name__, 'datadir'))

        cls.song_plugins = files.load_plugins(
            datadirs=cls.config['datadir'],
            root_modules=['songs'],
            keyword='SONG_RENDERERS',
            )
        for source in sorted(glob.glob(os.path.join(
                os.path.dirname(__file__),
                '*.source',
            ))):
            base = os.path.relpath(source, os.getcwd())[:-len(".source")]
            for dest in LANGUAGES:
                destname = "{}.{}".format(base, dest)
                if not os.path.exists(destname):
                    continue
                yield (
                    "test_{}_{}".format(os.path.basename(base), dest),
                    cls._create_test(base, dest),
                    )
                if os.path.basename(base) == 'newline':
                    yield (
                        "test_crlf_{}_{}".format(os.path.basename(base), dest),
                        cls._create_crlf_test(base, dest),
                        )


    @classmethod
    def _create_test(cls, base, dest):
        """Return a function testing that `base` compilation in `dest` format.
        """

        def test_parse_render(self):
            """Test that `base` is correctly parsed and rendered."""
            if base is None or dest is None:
                return
            destname = "{}.{}".format(base, dest)
            with open_read(destname) as expectfile:
                chordproname = "{}.source".format(base)
                with disable_logging():
                    self.assertMultiLineEqual(
                        self.song_plugins[LANGUAGES[dest]]['sgc'](chordproname, self.config).render(
                            output=chordproname,
                            ).strip(),
                        expectfile.read().strip(),
                        )

        test_parse_render.__doc__ = (
            "Test that '{base}' is correctly parsed and rendererd into '{format}' format."
            ).format(base=os.path.basename(base), format=dest)
        return test_parse_render

    @classmethod
    def _create_crlf_test(cls, base, dest):
        """Transform the `base` line endings into CRLF and test the compilation.
        """

        def test_parse_render(self):
            """Test that `base` is correctly parsed and rendered when line endings are CRLF.
            """
            if base is None or dest is None:
                return
            originalname = "{}.source".format(base)
            chordproname = "{}.crlf.source".format(base)
            with open_read(originalname) as originalfile:
                with open(chordproname, 'w') as chordprofile:
                    for line in originalfile:
                        chordprofile.write(line.replace('\n', '\r\n'))
            destname = "{}.{}".format(base, dest)
            with open_read(destname) as expectfile:
                with disable_logging():
                    self.assertMultiLineEqual(
                        self.song_plugins[LANGUAGES[dest]]['sgc'](chordproname, self.config).render(
                            output=chordproname,
                            ).strip(),
                        expectfile.read().strip(),
                        )
            os.remove(chordproname)

        test_parse_render.__doc__ = (
            "Test that '{base}' is correctly parsed and rendererd into '{format}' format with CRLF."
            ).format(base=os.path.basename(base), format=dest)
        return test_parse_render

