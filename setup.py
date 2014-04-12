#!/usr/bin/env python

"""Installation script for songbook.

$ python setup.py install
"""
from distutils.core import setup
from distutils.command.install import install as _install
from songbook_core import __STR_VERSION__

import sys
import os
import site


def link_songbook():
    if sys.platform.startswith('darwin'):
        source = os.path.join(site.PREFIXES[0],
                              'bin',
                              'songbook')
        dest = '/usr/local/bin/songbook'
        if os.path.isfile(dest):
            print("File {dest} already exist, skipping.".format(dest=dest))
        else:
            os.symlink(source, dest)
    elif sys.platform.startswith('win32'):
        script = os.path.join(site.PREFIXES[0],
                              'Scripts',
                              'songbook')
        dest = script + '.py'
        bat_name = script + '.bat'
        if os.path.isfile(dest):
            os.unlink(dest)
        os.rename(script, dest)
        content = "python {songbook} %* \n".format(songbook=dest)
        with open(bat_name, 'w') as bat_file:
            bat_file.write(content)


class install(_install):
    def run(self):
        _install.run(self)
        link_songbook()


setup(cmdclass={'install': install},
        name='songbook-core',
        version=__STR_VERSION__,
        description='Songbook compilation chain',
        author='The Songbook team',
        author_email='crep@team-on-fire.com',
        url='https://github.com/patacrep/songbook-core',
        packages=['songbook_core'],
        license="GPLv2 or any later version",
        scripts=['songbook'],
        requires=[
            "argparse", "codecs", "distutils", "fnmatch", "glob", "json",
            "locale", "logging", "os", "plasTeX", "re", "subprocess", "sys",
            "textwrap", "unidecode", "jinja2"
            ],
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
            "Operating System :: Microsoft :: Windows",
            "Operating System :: MacOS :: MacOS X"
            "Programming Language :: Python :: 2.7",
            "Topic :: Utilities",
            ],
        platforms=["GNU/Linux", "Windows", "MacOsX"],
)
