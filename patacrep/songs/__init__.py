"""Song management."""

import errno
import hashlib
import jinja2
import logging
import os
import pickle
import re

from patacrep.authors import process_listauthors
from patacrep import files, encoding
from patacrep.content import Content

LOGGER = logging.getLogger(__name__)

def cached_name(datadir, filename):
    """Return the filename of the cache version of the file."""
    fullpath = os.path.abspath(os.path.join(datadir, '.cache', filename))
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

# pylint: disable=too-many-instance-attributes
class Song(Content):
    """Song (or song metadata)

    This class represents a song, bound to a file.

    - It can parse the file given in arguments.
    - It can render the song as some LaTeX code.
    - Its content is cached, so that if the file has not been changed, the
      file is not parsed again.

    This class is inherited by classes implementing song management for
    several file formats. Those subclasses must implement:
    - `parse()` to parse the file;
    - `render()` to render the song as LaTeX code.
    """

    # Version format of cached song. Increment this number if we update
    # information stored in cache.
    CACHE_VERSION = 2

    # List of attributes to cache
    cached_attributes = [
        "titles",
        "unprefixed_titles",
        "cached",
        "data",
        "subpath",
        "languages",
        "authors",
        "_filehash",
        "_version",
        ]

    def __init__(self, datadir, subpath, config):
        self.fullpath = os.path.join(datadir, subpath)
        self.datadir = datadir
        self.encoding = config["encoding"]
        self.config = config

        if datadir:
            # Only songs in datadirs are cached
            self._filehash = hashlib.md5(
                open(self.fullpath, 'rb').read()
                ).hexdigest()
            if os.path.exists(cached_name(datadir, subpath)):
                try:
                    cached = pickle.load(open(
                        cached_name(datadir, subpath),
                        'rb',
                        ))
                    if (
                            cached['_filehash'] == self._filehash
                            and cached['_version'] == self.CACHE_VERSION
                    ):
                        for attribute in self.cached_attributes:
                            setattr(self, attribute, cached[attribute])
                        return
                except: # pylint: disable=bare-except
                    LOGGER.warning("Could not use cached version of {}.".format(
                        self.fullpath
                        ))

        # Data extraction from the latex song
        self.titles = []
        self.data = {}
        self.cached = None
        self.parse(config)

        # Post processing of data
        self.datadir = datadir
        self.subpath = subpath
        self.unprefixed_titles = [
            unprefixed_title(
                title,
                config['titleprefixwords']
                )
            for title
            in self.titles
            ]
        self.authors = process_listauthors(
            self.authors,
            **config["_compiled_authwords"]
            )

        # Cache management
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
                protocol=-1
                )

    def __repr__(self):
        return repr((self.titles, self.data, self.fullpath))

    def tex(self, output): # pylint: disable=no-self-use, unused-argument
        """Return the LaTeX code rendering this song.

        Arguments:
        - output: Name of the output file.
        """
        raise NotImplementedError()

    def parse(self, config): # pylint: disable=no-self-use
        """Parse song.

        It set the following attributes:

        - titles: the list of (raw) titles. This list will be processed to
          remove prefixes.
        - languages: the list of languages used in the song, as languages
          recognized by the LaTeX babel package.
        - authors: the list of (raw) authors. This list will be processed to
          'clean' it (see function :func:`patacrep.authors.processauthors`).
        - data: song metadata. Used (among others) to sort the songs.
        - cached: additional data that will be cached. Thus, data stored in
          this attribute must be picklable.
        """
        raise NotImplementedError()

def unprefixed_title(title, prefixes):
    """Remove the first prefix of the list in the beginning of title (if any).
    """
    for prefix in prefixes:
        match = re.compile(r"^(%s)\b\s*(.*)$" % prefix, re.LOCALE).match(title)
        if match:
            return match.group(2)
    return title
