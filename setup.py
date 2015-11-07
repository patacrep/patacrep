#!/usr/bin/env python3

"""Installation script for songbook.

$ python setup.py install
"""
from patacrep import __version__

from setuptools import setup, find_packages

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
        "unidecode", "jinja2", "ply",
        ],
    setup_requires=["hgtools"],
    package_data={'patacrep': [
        'data/ast_templates/*/*/*',
        'data/img/*',
        'data/latex/*',
        'data/templates/*',
        ]},
    entry_points={
        'console_scripts': [
            "songbook = patacrep.songbook.__main__:main",
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
)
