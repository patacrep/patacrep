"""Song management."""

import errno
import hashlib
import logging
import os
import pickle
import re

from patacrep import errors as book_errors
from patacrep import files, encoding
from patacrep.authors import process_listauthors
from patacrep.songs import errors as song_errors

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

class DataSubpath:
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
class Song:
    """Song (or song metadata)

    This class represents a song, bound to a file.

    - It can parse the file given in arguments.
    - It can render the song as some code (LaTeX, chordpro, depending on subclasses implemetation).
    - Its content is cached, so that if the file has not been changed, the
      file is not parsed again.

    This class is inherited by classes implementing song management for
    several file formats. Those subclasses must implement:
    - `parse()` to parse the file;
    - `render()` to render the song as code.
    """

    # Version format of cached song. Increment this number if we update
    # information stored in cache.
    CACHE_VERSION = 4

    # List of attributes to cache
    cached_attributes = [
        "titles",
        "unprefixed_titles",
        "cached",
        "data",
        "errors",
        "lang",
        "authors",
        "_filehash",
        "_version",
        ]

    def __init__(self, subpath, config=None, *, datadir=None):
        if config is None:
            config = {}

        if datadir is None:
            self.datadir = ""
            # Only songs in datadirs may be cached
            self.use_cache = False
        else:
            self.datadir = datadir
            self.use_cache = config.get('_cache', False)

        self.fullpath = os.path.join(self.datadir, subpath)
        self.subpath = subpath
        self._filehash = None
        self.encoding = config['book']["encoding"]
        self.lang = config['book']["lang"]
        self.config = config
        self.errors = []

        if self._cache_retrieved():
            return

        # Data extraction from the latex song
        self.titles = []
        self.data = {}
        self.cached = {}
        self._parse()

        # Post processing of data
        self.unprefixed_titles = [
            unprefixed_title(
                title,
                config['titles']['prefix']
                )
            for title
            in self.titles
            ]
        self.authors = process_listauthors(
            self.authors,
            **config.get("_compiled_authwords", {})
            )

        # Cache management
        self._version = self.CACHE_VERSION
        self._write_cache()

    @property
    def cached_name(self):
        """Name of the file used for the cache"""
        return cached_name(self.datadir, self.subpath)

    @property
    def filehash(self):
        """Compute (and cache) the md5 hash of the file"""
        if self._filehash is None:
            with open(self.fullpath, 'rb') as songfile:
                self._filehash = hashlib.md5(songfile.read()).hexdigest()
        return self._filehash

    def _cache_retrieved(self):
        """If relevant, retrieve self from the cache."""
        if self.use_cache and os.path.exists(self.cached_name):
            try:
                with open(self.cached_name, 'rb',) as cachefile:
                    cached = pickle.load(cachefile)
                if (
                        cached['_filehash'] == self.filehash
                        and cached['_version'] == self.CACHE_VERSION
                ):
                    for attribute in self.cached_attributes:
                        setattr(self, attribute, cached[attribute])
                    return True
            except: # pylint: disable=bare-except
                LOGGER.warning("Could not use cached version of {}.".format(
                    self.fullpath
                    ))
        return False

    def _write_cache(self):
        """If relevant, write a dumbed down version of self to the cache."""
        if not self.use_cache:
            return
        if self.errors:
            # As errors are exceptions, we cannot cache them because of a Python
            # bug. When this bug is fixed, we will cache errors.
            # https://bugs.python.org/issue1692335
            return
        cached = {attr: getattr(self, attr) for attr in self.cached_attributes}
        with open(self.cached_name, 'wb') as cache_file:
            pickle.dump(
                cached,
                cache_file,
                protocol=-1
                )

    def __str__(self):
        return str(self.fullpath)

    def render(self, *args, **kwargs):
        """Return the code rendering this song.

        Arguments:
        - output: Name of the output file, or `None` if irrelevant.
        """
        raise NotImplementedError()

    def _parse(self): # pylint: disable=no-self-use
        """Parse song.

        It set the following attributes:

        - titles: the list of (raw) titles. This list will be processed to
          remove prefixes.
        - lang: the main language of the song, as language code.
        - authors: the list of (raw) authors. This list will be processed to
          'clean' it (see function :func:`patacrep.authors.processauthors`).
        - data: song metadata. Used (among others) to sort the songs.
        - cached: additional data that will be cached. Thus, data stored in
          this attribute must be picklable.
        """
        raise NotImplementedError()

    def iter_datadirs(self, *subpath):
        """Return an iterator of existing datadirs (with an optionnal subpath)
        """
        yield from files.iter_datadirs(self.config['_datadir'], *subpath)

    def search_datadir_file(self, filename, extensions=None, directories=None):
        """Search for a file name.

        :param str filename: The name, as provided in the chordpro file (with or without extension).
        :param list extensions: Possible extensions (with '.'). Default is no extension.
        :param iterator directories: Other directories where to search for the file
                                The directory where the Song file is stored is added to the list.
        :return: A tuple `(datadir, filename, extension)` if file has been
            found. It is guaranteed that `os.path.join(datadir,
            filename+extension)` is a (relative or absolute) valid path to an
            existing filename.
            * `datadir` is the datadir in which the file has been found. Can be
                the empty string.
            * `filename` is the filename, relative to the datadir.
            * `extension` is the extension that is to be appended to the
                filename to get the real filename. Can be the empty string.

        Raise `FileNotFoundError` if nothing found.

        This function can also be used as a preprocessor for a renderer: for
        instance, it can compile a file, place it in a temporary folder, and
        return the path to the compiled file.
        """
        if extensions is None:
            extensions = ['']
        if directories is None:
            directories = self.config['_datadir']

        songdir = os.path.dirname(self.fullpath)
        for extension in extensions:
            if os.path.isfile(os.path.join(songdir, filename + extension)):
                return "", os.path.join(songdir, filename), extension

        for directory in directories:
            for extension in extensions:
                if os.path.isfile(os.path.join(directory, filename + extension)):
                    return directory, filename, extension

        raise FileNotFoundError(filename)

    def search_file(self, filename, extensions=None, *, datadirs=None):
        """Return the path to a file present in a datadir.

        Implementation is specific to each renderer, as:
        - some renderers can preprocess files;
        - some renderers can return the absolute path, other can return something else;
        - etc.
        """
        raise NotImplementedError()

    def search_image(self, filename):
        """Search for an image file"""
        return self.search_file(
            filename,
            ['', '.jpg', '.png'],
            datadirs=self.iter_datadirs('img'),
            )

    def search_partition(self, filename):
        """Search for a lilypond file"""
        return self.search_file(
            filename,
            ['', '.ly'],
            datadirs=self.iter_datadirs('scores'),
            )

def unprefixed_title(title, prefixes):
    """Remove the first prefix of the list in the beginning of title (if any).
    """
    for prefix in prefixes:
        match = re.compile(r"^(%s)\b\s*(.*)$" % prefix).match(title)
        if match:
            return match.group(2)
    return title
