"""Tests for the index generation."""

import codecs
import glob
import os
import unittest

from patacrep.index import process_sxd

from .. import dynamic # pylint: disable=unused-import


class FileTest(unittest.TestCase, metaclass=dynamic.DynamicTest):
    """Test of the index generation.

    For any given `foo.sxd`, it generates the index.
    It controls that the generated file is equal to the one in `foo.sbx`.
    """

    @classmethod
    def _iter_testmethods(cls):
        """Iterate over dynamically generated test methods"""
        for source in sorted(glob.glob(os.path.join(
                os.path.dirname(__file__),
                '*.sxd',
            ))):
            base = source[:-len(".sxd")]
            yield (
                "test_index_{}".format(os.path.basename(base)),
                cls._create_index_test(base),
                )

    @classmethod
    def _create_index_test(cls, base):
        """Return a function that tests that `foo.sxd` produces the sbx file"""

        def test_index(self):
            """Test that `foo.sxd` produces the correct sbx file"""
            generated_index = process_sxd(base + ".sxd").entries_to_str()
            with codecs.open(base + ".sbx", "r", "utf-8") as control_index:
                self.assertEqual(control_index.read(), generated_index, )

        test_index.__doc__ = (
            "Test that '{base}.sxd' produces the correct sbx file"""
            ).format(base=os.path.basename(base))
        return test_index
