Patacrep, a songbook compilation chain
======================================

|sources| |pypi| |documentation| |license|

|build-travis| |build-appveyor|

This package provides a compilation toolchain that produce LaTeX
songbook using the LaTeX songs package. A new LaTeX document class is
provided to allow specific customisation and new command like embedded
guitar tabs or lilypond sheets.

Document are subject to the GNU GPLv2 except if another license
is precised in the header.

Python version
--------------

Patacrep is only compatible with Python > 3.3.

Installation
------------

Using pip
^^^^^^^^^

For the stable version, as simple as::

    pip3 install patacrep

And upgrade to the latest release::

    pip3 install patacrep -U

Or for the latest version::

    pip3 install https://github.com/patacrep/patacrep/archive/master.zip

Details about the dependecies are in the `documentation <#documentation>`_.

For developement
^^^^^^^^^^^^^^^^

Clone Patacrep repos::

    git clone git://github.com/patacrep/patacrep.git
    cd patacrep
    pip3 install -r Requirements.txt
    python3 setup.py develop

Quick and dirty Debian (and Ubuntu?) package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

    python setup.py --command-packages=stdeb.command bdist_deb
    sudo dpkg -i deb_dist/python3-patacrep_4.0.0-1_all.deb

Run
---

::

    songbook <songbook_file.yaml>
    <pdfreader> <songbook_file.pdf>

Look for existing songbook files in `patadata <http://github.com/patacrep/patadata>`_.

Documentation
-------------

The full documentation is hosted by readthedoc, here : http://patacrep.readthedocs.org/ (currently only in french).

Toolchain overview
------------------

The following steps happen by default (see [build.py](https://github.com/patacrep/patacrep/blob/master/patacrep/build.py#L19):

1. `tex` generate a LaTeX file, based on the list of files mentionned in the songbook (a conversion to LaTeX formats happens for ChordPro files)
2. `pdf` generates a pdf, using `lualatex`
3. `sbx` make .sbx indexes from .sxd files
4. `pdf` generate a pdf again, with the index
5. `clean` removes the temporary files

Contact & Forums
----------------

* http://www.patacrep.com/forum

.. |documentation| image:: http://readthedocs.org/projects/patacrep/badge
  :target: http://patacrep.readthedocs.org
.. |pypi| image:: https://img.shields.io/pypi/v/patacrep.svg
  :target: http://pypi.python.org/pypi/patacrep
.. |license| image:: https://img.shields.io/pypi/l/patacrep.svg
  :target: http://www.gnu.org/licenses/gpl-2.0.html
.. |sources| image:: https://img.shields.io/badge/sources-patacrep-brightgreen.svg
  :target: http://github.com/patacrep/patacrep
.. |build-travis| image:: https://img.shields.io/travis-ci/patacrep/patacrep/master.svg?label=GNU/Linux
  :target: https://travis-ci.org/patacrep/patacrep/branches
.. |build-appveyor| image:: https://img.shields.io/appveyor/ci/oliverpool/patacrep/master.svg?label=Windows
  :target: https://ci.appveyor.com/project/oliverpool/patacrep/branch/master
