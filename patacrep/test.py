"""Tests"""

import contextlib
import doctest
import logging
import os
import unittest

import patacrep

@contextlib.contextmanager
def disable_logging():
    """Context locally disabling logging."""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)

def suite():
    """Return a TestSuite object, to test whole `patacrep` package.

    Both unittest and doctest are tested.
    """
    test_loader = unittest.defaultTestLoader
    return test_loader.discover(os.path.dirname(__file__))

def load_tests(__loader, tests, __pattern):
    """Load tests (unittests and doctests)."""
    # Loading doctests
    tests.addTests(doctest.DocTestSuite(patacrep))

    # Unittests are loaded by default
    return tests

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())

