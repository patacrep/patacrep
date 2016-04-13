#!/usr/bin/env python3

"""Installation script for songbook.

$ python setup.py install
"""
from patacrep import __version__

from setuptools import setup, find_packages
import sys

setup_kwargs = {
    'setup_requires': [],
    }

if sys.platform[0:3] == 'win':
    from patacrep import __DATADIR__, files

    # List the data files
    data_files = files.recursive_find(__DATADIR__)
    data_files = ["data/" + d for d in data_files]
    setup_kwargs['package_data'] = {'patacrep': data_files}
else:
    setup_kwargs['setup_requires'].append('hgtools')
    setup_kwargs['include_package_data'] = True

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
    long_description = open("README.rst", "r").read(),
    **setup_kwargs
)
