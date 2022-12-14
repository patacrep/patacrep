"""Tests for the content plugins."""

# pylint: disable=too-few-public-methods

import glob
import os
import unittest
import yaml

from pkg_resources import resource_filename

from patacrep import content, files
from patacrep.songbook import prepare_songbook

from .. import logging_reduced
from .. import dynamic # pylint: disable=unused-import

class FileTest(unittest.TestCase, metaclass=dynamic.DynamicTest):
    """Test of the content plugins.

    For any given `foo.source`, it parses the content as a yaml "content"
    argument of a .yaml file.
    It controls that the generated file list is equal to the one in `foo.control`.
    """

    maxDiff = None
    config = None

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
        """Return a function that tests that `base.source` produces the correct file list"""

        def test_content(self):
            """Test that `base.source` produces the correct file list"""
            sourcename = "{}.source".format(base)
            with open(sourcename, mode="r", encoding="utf8") as sourcefile:
                sbcontent = yaml.safe_load(sourcefile)

            outputdir = os.path.dirname(base)
            config = cls._generate_config(sbcontent, outputdir, base)

            with logging_reduced('patacrep.content.song'):
                expandedlist = content.process_content(sbcontent, config)
            sourcelist = [cls._clean_path(elem.to_dict()) for elem in expandedlist]

            controlname = "{}.control".format(base)
            if not os.path.exists(controlname):
                raise Exception("Missing control:" + str(controlname).replace("'", '"'))
            with open(controlname, mode="r", encoding="utf8") as controlfile:
                controllist = yaml.safe_load(controlfile)

            self.assertEqual(controllist, sourcelist)

        test_content.__doc__ = (
            "Test that '{base}.source' produces the correct file list"""
            ).format(base=os.path.basename(base))
        return test_content

    @classmethod
    def _clean_path(cls, elem):
        """Shorten the path relative to the test directory"""
        if not isinstance(elem, dict):
            return elem

        test_path = files.path2posix(resource_filename(__name__, ""))+"/"
        for key in ['song', 'tex']:
            if key in elem:
                elem[key] = files.path2posix(
                    os.path.normpath(elem[key])
                ).replace(test_path, "")
        return elem

    @classmethod
    def _generate_config(cls, sbcontent, outputdir, base):
        """Generate the config to process the content"""

        # Load the default songbook config
        config = prepare_songbook(
            {'book':{'datadir':['datadir', 'datadir_zippedcontent']}, 'content': sbcontent},
            outputdir,
            base,
            outputdir
            )

        return config
