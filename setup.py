#!/usr/bin/env python

"""Installation script for songbook.

$ python setup.py install
"""
from distutils.core import setup

import songbook_core

setup(name='songbook-core',
        version=songbook_core.__STR_VERSION__,
        description='Songbook compilation chain',
        author='The Songbook team',
        author_email='crep@team-on-fire.com',
        url='https://github.com/patacrep/songbook-core',
        scripts=['songbook'],
        license="GPLv2 or any later version",
        requires=[
            "argparse", "codecs", "distutils", "fnmatch", "glob", "json",
            "locale", "logging", "os", "plasTeX", "re", "subprocess", "sys",
            "textwrap", "unidecode"
            ],
        packages=['songbook_core'],
        package_data={'songbook_core': ['data/latex/*',
                                        'data/templates/*',
                                        'data/examples/*.sb',
                                        'data/examples/*/*.sg',
                                        'data/examples/*/*.ly',
                                        'data/examples/*/*.jpg',
                                        'data/examples/*/*.png',
                                        'data/examples/*/*.png',
                                        'data/examples/*/*/header']},
        classifiers=[
            "Environment :: Console",
            "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
            "Natural Language :: English",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 2.7",
            "Topic :: Utilities",
            ],
        platforms=["GNU/Linux"],
)
