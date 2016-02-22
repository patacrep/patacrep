"""Tests of the patatools-cache command."""

# pylint: disable=too-few-public-methods

import os
import shutil
import unittest

from patacrep.files import chdir
from patacrep.tools.__main__ import main as tools_main
from patacrep.tools.cache.__main__ import main as cache_main
from patacrep.songbook.__main__ import main as songbook_main

from .. import logging_reduced

CACHEDIR = os.path.join(os.path.dirname(__file__), "test_cache_datadir", ".cache")

class TestCache(unittest.TestCase):
    """Test of the "patatools cache" subcommand"""

    def setUp(self):
        """Remove cache."""
        self._remove_cache()
        self.assertFalse(os.path.exists(CACHEDIR))

    def tearDown(self):
        """Remove cache."""
        self._remove_cache()
        self.assertFalse(os.path.exists(CACHEDIR))

    @staticmethod
    def _remove_cache():
        """Delete cache."""
        shutil.rmtree(CACHEDIR, ignore_errors=True)

    def _system(self, main, args):
        with chdir(os.path.dirname(__file__)):
            try:
                main(args)
            except SystemExit as systemexit:
                self.assertEqual(systemexit.code, 0)

    def test_clean_exists(self):
        """Test of the "patatools cache clean" subcommand"""
        for main, args in [
                (tools_main, ["patatools", "cache", "clean", "test_cache.yaml"]),
                (cache_main, ["patatools-cache", "clean", "test_cache.yaml"]),
            ]:
            with self.subTest(main=main, args=args):
                # First compilation. Ensure that cache exists afterwards
                with logging_reduced('patacrep.build'):
                    self._system(
                        songbook_main,
                        ["songbook", "--steps", "tex,clean", "test_cache.yaml"]
                    )
                self.assertTrue(os.path.exists(CACHEDIR))

                # Clean cache
                with logging_reduced('patatools.cache'):
                    self._system(main, args)

                # Ensure that cache does not exist
                self.assertFalse(os.path.exists(CACHEDIR))

    def test_clean_not_exists(self):
        """Test of the "patatools cache clean" subcommand"""
        # Clean non-existent cache
        for main, args in [
                (tools_main, ["patatools", "cache", "clean", "test_cache.yaml"]),
                (cache_main, ["patatools-cache", "clean", "test_cache.yaml"]),
            ]:
            with self.subTest(main=main, args=args):
                # Clean cache
                with logging_reduced('patatools.cache'):
                    self._system(main, args)
