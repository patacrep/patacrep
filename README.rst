Patacrep, a songbook compilation chain
======================================

|build-travis| |build-appveyor|

This package provides a compilation toolchain that produce LaTeX
songbook using the LaTeX songs package. A new LaTeX document class is
provided to allow specific customisation and new command like embedded
guitar tabs or lilypond sheets.

|license|

Document are subject to the GNU GPLv2 except if another licence
is precised in the header.

Python version
--------------

Patacrep is only compatible with Python > 3.3.

Installation
------------

Using pip |pypi|
^^^^^^^^^^^^^^^^

As simple as::

    pip3 install patacrep

For developement |sources|
^^^^^^^^^^^^^^^^^^^^^^^^^^

Clone Patacrep repos::

    git clone git://github.com/patacrep/patacrep.git
    cd patacrep
    pip3 install -r Requirements.txt
    python3 setup.py install

Quick and dirty Debian (and Ubuntu?) package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

    python setup.py --command-packages=stdeb.command bdist_deb
    sudo dpkg -i deb_dist/python3-patacrep_4.0.0-1_all.deb

Run
---

::

    songbook <songbook_file.sb>
    <pdfreader> <songbook_file.pdf>

Look for existing songbook files in `patadata <http://github.com/patacrep/patadata>`_.

Documentation |documentation|
-----------------------------

The full documentation is hosted by readthedoc, here : http://patacrep.readthedocs.org/.

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
.. |build-travis| image:: https://img.shields.io/travis-ci/patacrep/patacrep.svg?branch=master&label=GNU/Linux
  :target: https://travis-ci.org/patacrep/patacrep
.. |build-appveyor| image:: https://img.shields.io/appveyor/ci/oliverpool/patacrep.svg?branch=master&label=Windows
  :target: https://ci.appveyor.com/project/oliverpool/patacrep
