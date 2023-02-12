#!/usr/bin/env python3

"""Installation script for songbook.

$ python setup.py install
"""
from patacrep import __version__, __DATADIR__

from setuptools import setup, find_packages
import os


setup_kwargs = {
    'setup_requires': [],
    }


def recursive_find(root_directory):
    """Recursively find files from a root_directory.

    Return a list of files matching those conditions.

    Arguments:
    - `root_directory`: root directory of the search.
    """
    if not os.path.isdir(root_directory):
        return

    olddir = os.getcwd()
    os.chdir(root_directory)
    for root, _, filenames in os.walk(os.curdir):
        for filename in filenames:
            yield os.path.join(root, filename)
    os.chdir(olddir)


# List the data files
data_files = recursive_find(__DATADIR__)
data_files = ["data/" + d for d in data_files]
setup_kwargs['package_data'] = {'patacrep': data_files}


setup(
    name='patacrep',
    version=__version__,
    description='Songbook compilation chain',
    author='The Songbook team',
    author_email='crep@team-on-fire.com',
    url='https://github.com/patacrep/patacrep',
    packages=find_packages(exclude=["test*"]),
    license="GPLv2 or any later version",
    install_requires=[
        "argdispatch", "unidecode", "jinja2", "ply", "pyyaml",
        ],
    entry_points={
        'console_scripts': [
            "songbook = patacrep.songbook.__main__:main",
            "patatools = patacrep.tools.__main__:main",
            ],
        },
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Utilities",
        ],
    platforms=["GNU/Linux", "Windows", "MacOsX"],
    test_suite="test.suite",
    long_description=open("README.rst", "r").read(),
    **setup_kwargs
)
