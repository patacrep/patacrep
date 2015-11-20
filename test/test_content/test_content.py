"""Tests for the content plugins."""

# pylint: disable=too-few-public-methods

import glob
import os
import unittest
import json

from patacrep.songs import DataSubpath, DEFAULT_CONFIG
from patacrep import content, files
from patacrep.content import song, section, songsection

from .. import dynamic # pylint: disable=unused-import

class FileTest(unittest.TestCase, metaclass=dynamic.DynamicTest):
    """Test of the content plugins.

    For any given `foo.source`, it parses the content as a json "content"
    argument of a .sb file.
    It controls that the generated file list is equal to the one in `foo.control`.
    """

    maxDiff = None
    config = None

    @classmethod
    def setUpClass(cls):
        cls._generate_config()

    @classmethod
    def _iter_testmethods(cls):
        """Iterate over dynamically generated test methods"""
        for source in sorted(glob.glob(os.path.join(
                os.path.dirname(__file__),
                '*.source',
            ))):
            base = source[:-len(".source")]
            yield (
                "test_content_{}".format(os.path.basename(base)),
                cls._create_content_test(base),
                )

    @classmethod
    def _create_content_test(cls, base):
        """Return a function that `base.source` produces the correct file list"""

        def test_content(self):
            """Test that `base.source` produces the correct file list"""
            sourcename = "{}.source".format(base)
            with open(sourcename, mode="r", encoding="utf8") as sourcefile:
                sbcontent = json.load(sourcefile)

            expandedlist = content.process_content(sbcontent, cls.config.copy())
            sourcelist = [cls._clean_path(elem) for elem in expandedlist]

            controlname = "{}.control".format(base)
            if not os.path.exists(controlname):
                raise Exception("Missing control:" + str(sourcelist).replace("'", '"'))
            with open(controlname, mode="r", encoding="utf8") as controlfile:
                controllist = json.load(controlfile)

            self.assertEqual(controllist, sourcelist)

        test_content.__doc__ = (
            "Test that '{base}.source' produces the correct file list"""
            ).format(base=os.path.basename(base))
        return test_content

    @classmethod
    def _clean_path(cls, elem):
        """Shorten the path relative to the `songs` directory"""
        if isinstance(elem, song.SongRenderer):
            songpath = os.path.join(os.path.dirname(__file__), 'datadir', 'songs')
            return files.path2posix(files.relpath(elem.song.fullpath, songpath))

        elif isinstance(elem, section.Section):
            if elem.short is None:
                return "{}:{}".format(elem.keyword, elem.name)
            else:
                return "{}:({}){}".format(elem.keyword, elem.short, elem.name)

        elif isinstance(elem, songsection.SongSection):
            return "{}:{}".format(elem.keyword, elem.name)

        else:
            raise Exception(elem)

    @classmethod
    def _generate_config(cls):
        """Generate the config to process the content"""

        config = DEFAULT_CONFIG.copy()

        datadirpaths = [os.path.join(os.path.dirname(__file__), 'datadir')]

        config['datadir'] = datadirpaths

        config['_songdir'] = [
            DataSubpath(path, 'songs')
            for path in datadirpaths
            ]
        config['_content_plugins'] = files.load_plugins(
            datadirs=datadirpaths,
            root_modules=['content'],
            keyword='CONTENT_PLUGINS',
            )
        config['_song_plugins'] = files.load_plugins(
            datadirs=datadirpaths,
            root_modules=['songs'],
            keyword='SONG_RENDERERS',
            )['tsg']
        cls.config = config
