"""File system utilities."""

from contextlib import contextmanager
import logging
import os
import pkgutil
import posixpath
import re
import sys

from patacrep import utils
from patacrep import __DATADIR__

LOGGER = logging.getLogger(__name__)

def recursive_find(root_directory, extensions=None):
    """Recursively find files with the given extensions, from a root_directory.

    Return a list of files matching those conditions.

    Arguments:
    - `extensions`: list of accepted extensions (None means every file).
    - `root_directory`: root directory of the search.
    """
    if not os.path.isdir(root_directory):
        return []

    matches = []
    if extensions is None:
        pattern = re.compile('.*')
    else:
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
        tail,
        )

@contextmanager
def chdir(*path):
    """Locally change dir

    Can be used as:

        with chdir("some", "directory"):
            do_stuff()
    """
    olddir = os.getcwd()
    if path:
        os.chdir(os.path.join(*path))
        yield
        os.chdir(olddir)
    else:
        yield

def iter_modules(path, prefix):
    """Iterate over modules located in list of `path`.

    Prefix is a prefix appended to all module names.
    """
    for module_finder, name, __is_pkg in pkgutil.walk_packages(path, prefix):
        if name in sys.modules:
            yield sys.modules[name]
        else:
            try:
                yield module_finder.find_spec(name).loader.load_module()
            except ImportError as error:
                LOGGER.debug("[plugins] Could not load module {}: {}".format(name, str(error)))
                continue

def load_plugins(datadirs, root_modules, keyword):
    """Load all plugins, and return a dictionary of those plugins.

    A plugin is a .py file, submodule of `subdir`, located in one of the
    directories of `datadirs`. It contains a dictionary `keyword`. The return
    value is the union of the dictionaries of the loaded plugins.

    Arguments:
    - datadirs: List of directories in which plugins are to be searched.
    - root_modules: the submodule in which plugins are to be searched, as a
      list of modules (e.g. ["some", "deep", "module"] for
      "some.deep.module").
    - keyword: attribute containing plugin information.

    Return value: a dictionary where:
    - keys are the keywords ;
    - values are functions triggered when this keyword is met.
    """
    plugins = utils.DictOfDict()

    datadir_path = [
        os.path.join(datadir, "python", *root_modules)
        for datadir
        in datadirs
        ]
    sys_path = [
        os.path.join(path, "patacrep", *root_modules)
        for path
        in sys.path
        ]
    for module in iter_modules(
            datadir_path + sys_path,
            prefix="patacrep.{}.".format(".".join(root_modules))
        ):
        if hasattr(module, keyword):
            plugins.update(getattr(module, keyword))
    return plugins

def iter_datadirs(datadirs, *subpath):
    """Iterate over datadirs.

    The default datadir is returned last.

    Subpath are appended after each datadir.
    """
    for path in datadirs:
        yield os.path.join(path, *subpath)
    yield os.path.join(__DATADIR__, *subpath)
