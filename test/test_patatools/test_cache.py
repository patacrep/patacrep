"""Tests of the patatools-convert command."""

# pylint: disable=too-few-public-methods

import os
import shutil
import unittest

from patacrep.tools import convert

CACHEDIR = os.path.join(os.path.dirname(__file__), "test_cache_datadir", "songs", ".cache")

class TestCache(unittest.TestCase):
    """Test of the "patatools cache" subcommand"""

    def setUp(self):
        """Remove cache."""
        self._remove_cache()

    def tearDown(self):
        """Remove cache."""
        self._remove_cache()

    def _remove_cache(self):
        """Delete cache."""
        shutil.rmtree(CACHEDIR, ignore_errors=True)

    def test_clean(self):
        """Test of the "patatools cache clean" subcommand"""
        # Cache does not exist
        self.assertFalse(os.path.exists(CACHEDIR))

        # First compilation. Ensure that cache exists afterwards
        TODO
        self.assertTrue(os.path.exists(CACHEDIR))

        # Clean cache
        TODO

        # Ensure that cache does not exist
        self.assertFalse(os.path.exists(CACHEDIR))
