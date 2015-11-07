"""Dealing with encoding problems."""

import codecs
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
        encoding = detect_encoding(filename)

    with codecs.open(
        filename,
        mode=mode,
        encoding=encoding,
        errors='replace',
        ) as fileobject:
        yield fileobject

def detect_encoding(filename):
    """Return the most likely encoding of the file
    """
    encodings = ['utf-8', 'windows-1250', 'windows-1252']
    for e in encodings:
        try:
            fh = codecs.open(filename, 'r', encoding=e)
            fh.readlines()
            fh.seek(0)
        except UnicodeDecodeError:
            pass
        else:
            if e != 'utf-8':
                print('Opening `%s` with `%s` encoding' % (filename, e))
            return e
        finally:
            fh.close()

    raise Exception('Not suitable encoding found for {}'.format(filename))
