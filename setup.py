#!/usr/bin/env python

"""Installation script for songbook.

$ python setup.py install
"""
from patacrep import __STR_VERSION__

import sys
import os
import site


SETUP = {"name": 'songbook-core',
        "version": __STR_VERSION__,
        "description": 'Songbook compilation chain',
        "author": 'The Songbook team',
        "author_email": 'crep@team-on-fire.com',
        "url": 'https://github.com/patacrep/songbook-core',
        "packages": ['patacrep'],
        "license": "GPLv2 or any later version",
        "scripts": ['songbook'],
        "requires": [
            "argparse", "codecs", "distutils", "fnmatch", "glob", "json",
            "locale", "logging", "os", "plasTeX", "re", "subprocess", "sys",
            "textwrap", "unidecode", "jinja2", "chardet"
            ],
        "package_data": {'patacrep': [  'data/latex/*',
                                        'data/templates/*',
                                        'data/examples/*.sb',
                                        'data/examples/*/*.sg',
                                        'data/examples/*/*.ly',
                                        'data/examples/*/*.jpg',
                                        'data/examples/*/*.png',
                                        'data/examples/*/*.png',
                                        'data/examples/*/*/header']},
        "classifiers": [
            "Environment :: Console",
            "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
            "Natural Language :: English",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: MacOS :: MacOS X"
            "Programming Language :: Python :: 2.7",
            "Topic :: Utilities",
            ],
        "platforms": ["GNU/Linux", "Windows", "MacOsX"]
}

if sys.platform.startswith('win32'):
    try:
        from cx_Freeze import setup, Executable
        exe = Executable(script="songbook")
    except ImportError:
        # Only a source installation will be possible
        from distutils.core import setup
        exe = None
    build_options = {'build_exe': {
                        "include_files": ["plasTeX/", "patacrep/"],
                        "excludes": ["plasTeX"],
                        "includes": ["UserList", "UserString", "new", "ConfigParser"]
                    }}
    SETUP.update({"options": build_options,
                "executables": [exe],
                "package_data": {},
            })
else:
    from distutils.core import setup


setup(**SETUP)
