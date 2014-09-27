# -*- coding: utf-8 -*-

"""Dealing with encoding problems."""

import codecs
import chardet
import logging

LOGGER = logging.getLogger(__name__)

def open_read(filename, mode='r'):
    """Open a file for reading, guessing the right encoding.

    Return a fileobject, reading unicode strings.
    """
    return codecs.open(
            filename,
            mode=mode,
            encoding=chardet.detect(open(filename, 'rb').read())['encoding'],
            errors='replace',
            )
