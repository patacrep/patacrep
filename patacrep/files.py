"""File system utilities."""

from contextlib import contextmanager
import glob
import importlib
import logging
import os
import posixpath
import re
import sys

LOGGER = logging.getLogger(__name__)

def recursive_find(root_directory, extensions):
    """Recursively find files with some extension, from a root_directory.

    Return a list of files matching those conditions.

    Arguments:
    - `extensions`: list of accepted extensions.
    - `root_directory`: root directory of the search.
    """
    if not os.path.isdir(root_directory):
        return []

    matches = []
    pattern = re.compile(r'.*\.({})$'.format('|'.join(extensions)))
    with chdir(root_directory):
        for root, __ignored, filenames in os.walk(os.curdir):
            for filename in filenames:
                if pattern.match(filename):
                    matches.append(os.path.join(root, filename))
    return matches

def relpath(path, start=None):
    """Return relative filepath to path if a subpath of start."""
    if start is None:
        start = os.curdir
    if os.path.abspath(path).startswith(os.path.abspath(start)):
        return os.path.relpath(path, start)
    else:
        return os.path.abspath(path)


def path2posix(string):
    """"Convert path from local format to posix format."""
    if not string or string == "/":
        return string
    if os.path.splitdrive(string)[1] == "\\":
        # Assuming DRIVE:\
        return string[0:-1]
    (head, tail) = os.path.split(string)
    return posixpath.join(
            path2posix(head),
            tail)

@contextmanager
def chdir(path):
    """Locally change dir

    Can be used as:

        with chdir("some/directory"):
            do_stuff()
    """
    olddir = os.getcwd()
    if path:
        os.chdir(path)
        yield
        os.chdir(olddir)
    else:
        yield

def load_plugins(datadirs, subdir, variable, error):
    """Load all content plugins, and return a dictionary of those plugins.

    A plugin is a .py file, submodule of `subdir`, located in one of the
    directories of `datadirs`. It contains a dictionary `variable`. The return
    value is the union of the dictionaries of the loaded plugins.

    Arguments:
    - datadirs: list of directories (as strings) in which files has to be
      searched.
    - subdir: modules (as a list of strings) files has to be submodules of
      (e.g. if `subdir` is `['first', 'second']`, search files are of the form
      `first/second/*.py`.
    - variable: Name of the variable holding the dictionary.
    - error: Error message raised if a key appears several times.
    """
    plugins = {}
    directory_list = (
            [
                os.path.join(datadir, "python", *subdir) #pylint: disable=star-args
                for datadir in datadirs
            ]
            + [os.path.dirname(__file__)]
            )
    for directory in directory_list:
        if not os.path.exists(directory):
            LOGGER.debug(
                    "Ignoring non-existent directory '%s'.",
                    directory
                    )
            continue
        sys.path.append(directory)
        for name in glob.glob(os.path.join(directory, *(subdir + ['*.py']))):
            if name.endswith(".py") and os.path.basename(name) != "__init__.py":
                if directory == os.path.dirname(__file__):
                    plugin = importlib.import_module(
                            'patacrep.{}.{}'.format(
                                ".".join(subdir),
                                os.path.basename(name[:-len('.py')])
                                )
                            )
                else:
                    plugin = importlib.import_module(
                                os.path.basename(name[:-len('.py')])
                                )
                for (key, value) in getattr(plugin, variable, {}).items():
                    if key in plugins:
                        LOGGER.warning(
                                error.format(
                                filename=relpath(name),
                                key=key,
                                )
                                )
                        continue
                    plugins[key] = value
        del sys.path[-1]
    return plugins


