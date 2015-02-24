"""File system utilities."""

from contextlib import contextmanager
import importlib
import logging
import os
import posixpath
import re

LOGGER = logging.getLogger(__name__)

def recursive_find(root_directory, extensions):
    """Recursively find files with the given extensions, from a root_directory.

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
    # pylint: disable=star-args
    plugins = {}
    directory_list = (
            [
                os.path.join(datadir, "python", *root_modules)
                for datadir in datadirs
            ]
            + [os.path.join(
                os.path.dirname(__file__),
                *root_modules
                )]
            )
    for directory in directory_list:
        if not os.path.exists(directory):
            LOGGER.debug(
                    "Ignoring non-existent directory '%s'.",
                    directory
                    )
            continue
        for (dirpath, __ignored, filenames) in os.walk(directory):
            modules = ["patacrep"] + root_modules
            if os.path.relpath(dirpath, directory) != ".":
                modules.extend(os.path.relpath(dirpath, directory).split("/"))
            for name in filenames:
                if name == "__init__.py":
                    modulename = []
                elif name.endswith(".py"):
                    modulename = [name[:-len('.py')]]
                else:
                    continue
                plugin = importlib.import_module(".".join(modules + modulename))
                if hasattr(plugin, keyword):
                    for (key, value) in getattr(plugin, keyword).items():
                        if key in plugins:
                            LOGGER.warning(
                                "File %s: Keyword '%s' is already used. Ignored.",
                                relpath(os.path.join(dirpath, name)),
                                key,
                                )
                            continue
                        plugins[key] = value
    return plugins
