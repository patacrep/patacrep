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
    """Return a :class:`TestSuite` object, testing all module :mod:`patacrep`.
    """
    test_loader = unittest.defaultTestLoader
    return test_loader.discover(
        os.path.abspath(os.path.dirname(__file__)),
        pattern="*.py",
        top_level_dir=os.path.abspath(os.path.join(patacrep.__path__[0], "..")),
        )

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())

