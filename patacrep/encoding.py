# -*- coding: utf-8 -*-

"""Dealing with encoding problems."""

import codecs
import chardet
import logging
from unidecode import unidecode as unidecode_orig

LOGGER = logging.getLogger(__name__)

def open_read(filename, mode='r'):
    """Open a file for reading, guessing the right encoding.

    Return a fileobject, reading unicode strings.
    """
    return codecs.open(
            filename,
            mode=mode,
            encoding=chardet.detect(open(filename, "r").read())['encoding'],
            errors='replace',
            )

def basestring2unicode(arg):
    """Return the unicode version of the argument, guessing original encoding.
    """
    if isinstance(arg, unicode):
        return arg
    elif isinstance(arg, basestring):
        return arg.decode(
                encoding=chardet.detect(arg)['encoding'],
                errors='replace',
                )
    else:
        LOGGER.warning("Cannot decode string {}. Ignored.".format(str(arg)))
        return ""

def list2unicode(arg):
    """Return the unicode version of the argument, guessing original encoding.

    Argument is a list of strings.  If an item is of another type, it is
    silently ignored (an empty string is returned).
    """
    return [basestring2unicode(item) for item in arg]

def unidecode(arg):
    """Return a unicode version of a unidecoded string."""
    return unicode(unidecode_orig(arg))
