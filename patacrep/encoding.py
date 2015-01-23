"""Dealing with encoding problems."""

import codecs
import chardet
import logging
import contextlib

LOGGER = logging.getLogger(__name__)


@contextlib.contextmanager
def open_read(filename, mode='r', encoding=None):
    """Open a file for reading, guessing the right encoding.

    Return a fileobject, reading unicode strings.
    If `encoding` is set, use it as the encoding (do not guess).
    """
    if encoding is None:
        fileencoding = chardet.detect(open(filename, 'rb').read())['encoding']
    else:
        fileencoding = encoding

    with codecs.open(
            filename,
            mode=mode,
            encoding=fileencoding,
            errors='replace',
            ) as fileobject:
        yield fileobject
