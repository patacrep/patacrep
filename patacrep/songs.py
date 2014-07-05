#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Song management."""

from unidecode import unidecode
import errno
import hashlib
import os
import re

try:
    import cPickle as pickle
except ImportError:
    import pickle

from patacrep.authors import processauthors
from patacrep.plastex import parsetex


def cached_name(datadir, filename):
    """Return the filename of the cache version of the file."""
    fullpath = os.path.join(datadir, '.cache', filename)
    directory = os.path.dirname(fullpath)
    try:
        os.makedirs(directory)
    except OSError as error:
        if error.errno == errno.EEXIST and os.path.isdir(directory):
            pass
        else:
            raise
    return fullpath

class DataSubpath(object):
    """A path divided in two path: a datadir, and its subpath.

    - This object can represent either a file or directory.
    - If the datadir part is the empty string, it means that the represented
      path does not belong to a datadir.
    """

    def __init__(self, datadir, subpath):
        if os.path.isabs(subpath):
            self.datadir = ""
        else:
            self.datadir = datadir
        self.subpath = subpath

    def __str__(self):
        return os.path.join(self.datadir, self.subpath)

    @property
    def fullpath(self):
        """Return the full path represented by self."""
        return os.path.join(self.datadir, self.subpath)

    def clone(self):
        """Return a cloned object."""
        return DataSubpath(self.datadir, self.subpath)

    def join(self, path):
        """Join "path" argument to self path.

        Return self for commodity.
        """
        self.subpath = os.path.join(self.subpath, path)
        return self

# pylint: disable=too-few-public-methods, too-many-instance-attributes
class Song(object):
    """Song management"""

    # Version format of cached song. Increment this number if we update
    # information stored in cache.
    CACHE_VERSION = 0

    # List of attributes to cache
    cached_attributes = [
            "titles",
            "unprefixed_titles",
            "args",
            "datadir",
            "fullpath",
            "subpath",
            "languages",
            "authors",
            "_filehash",
            "_version",
            ]

    def __init__(self, datadir, subpath, config):
        self.fullpath = os.path.join(datadir, subpath)
        if datadir:
            # Only songs in datadirs are cached
            self._filehash = hashlib.md5(
                    open(self.fullpath, 'rb').read()
                    ).hexdigest()
            if os.path.exists(cached_name(datadir, subpath)):
                cached = pickle.load(open(cached_name(datadir, subpath), 'rb'))
                if (
                        cached['_filehash'] == self._filehash
                        and cached['_version'] == self.CACHE_VERSION
                        ):
                    for attribute in self.cached_attributes:
                        setattr(self, attribute, cached[attribute])
                    return

        # Data extraction from the song with plastex
        data = parsetex(self.fullpath)
        self.titles = data['titles']
        self.datadir = datadir
        self.unprefixed_titles = [
                unprefixed_title(
                    unidecode(unicode(title, "utf-8")),
                    config['titleprefixwords']
                    )
                for title
                in self.titles
                ]
        self.args = data['args']
        self.subpath = subpath
        self.languages = data['languages']
        if "by" in self.args.keys():
            self.authors = processauthors(
                    self.args["by"],
                    **config["_compiled_authwords"]
                    )
        else:
            self.authors = []

        self._version = self.CACHE_VERSION
        self._write_cache()

    def _write_cache(self):
        """If relevant, write a dumbed down version of self to the cache."""
        if self.datadir:
            cached = {}
            for attribute in self.cached_attributes:
                cached[attribute] = getattr(self, attribute)
            pickle.dump(
                    cached,
                    open(cached_name(self.datadir, self.subpath), 'wb'),
                    )

    def __repr__(self):
        return repr((self.titles, self.args, self.fullpath))

def unprefixed_title(title, prefixes):
    """Remove the first prefix of the list in the beginning of title (if any).
    """
    for prefix in prefixes:
        match = re.compile(r"^(%s)\b\s*(.*)$" % prefix, re.LOCALE).match(title)
        if match:
            return match.group(2)
    return title


