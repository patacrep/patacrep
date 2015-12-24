"""Tests"""

import contextlib
import doctest
import logging
import os
import unittest

import patacrep

@contextlib.contextmanager
def logging_reduced(module_name=None, level=logging.CRITICAL):
    """Temporarly reduce the logging level of a specific module or globally if None
    """
    logger = logging.getLogger(module_name)
    old_level = logger.getEffectiveLevel()

    logger.setLevel(level)
    yield
    logger.setLevel(old_level)

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

