#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Song management."""

from unidecode import unidecode
import hashlib
import os
import re

try:
        import cPickle as pickle
except ImportError:
        import pickle

from patacrep.authors import processauthors
from patacrep.plastex import parsetex


def cached_name(filename):
    """Return the filename of the cache version of the file."""
    return filename + ".cache"

# pylint: disable=too-few-public-methods, too-many-instance-attributes
class Song(object):
    """Song management"""

    # Version format of cached song.
    CACHE_VERSION = 0

    # List of attributes to cache
    cached_attributes = [
            "titles",
            "unprefixed_titles",
            "args",
            "path",
            "languages",
            "authors",
            "_filehash",
            "_version",
            ]

    def __init__(self, filename, config):
        self._filehash = hashlib.md5(open(filename, 'rb').read()).hexdigest()
        if os.path.exists(cached_name(filename)):
            cached = pickle.load(open(cached_name(filename), 'rb'))
            if (
                    cached['_filehash'] == self._filehash
                    and cached['_version'] == self.CACHE_VERSION
                    ):
                for attribute in self.cached_attributes:
                    setattr(self, attribute, cached[attribute])
                return

        # Data extraction from the song with plastex
        data = parsetex(filename)
        self.titles = data['titles']
        self.unprefixed_titles = [
                unprefixed_title(
                    unidecode(unicode(title, "utf-8")),
                    config['titleprefixwords']
                    )
                for title
                in self.titles
                ]
        self.args = data['args']
        self.path = filename
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
        """Write a dumbed down version of self to the cache."""
        cached = {}
        for attribute in self.cached_attributes:
            cached[attribute] = getattr(self, attribute)
        pickle.dump(cached, open(cached_name(self.path), 'wb'))

    def __repr__(self):
        return repr((self.titles, self.args, self.path))

def unprefixed_title(title, prefixes):
    """Remove the first prefix of the list in the beginning of title (if any).
    """
    for prefix in prefixes:
        match = re.compile(r"^(%s)\b\s*(.*)$" % prefix, re.LOCALE).match(title)
        if match:
            return match.group(2)
    return title


