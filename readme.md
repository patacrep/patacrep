Songbook Compilation Chain

# Description

This package provides a compilation toolchain that produce LaTeX
songbook using the LaTeX songs package. A new LaTeX document class is
provided to allow specific customisation and new command like embedded
guitar tabs or lilypond sheets.

This package is distribued along with a songbook written and designed
by Crep (R. Goffe). This part of the package is provided with respect
to the CC-BY-SA licence.

Other document are subject to the GNU GPLv2 except if another licence
is precised in the header.

# Python version

Patacrep is compatible with Python 2.7 (no Python3 since [one of the
library](http://plastex.sourceforge.net/) we are using is not).

# Download

Clone Patacrep repos:

>     git clone git://github.com/patacrep/patacrep.git
>     git clone git://github.com/patacrep/patadata.git

# Run

>     <patacrep>/songbook <songbook_file.sb>
>     <pdfreader> <songbook_file.pdf>

Look for existing songbook files in `<patadata>/books/`. For example:

>     <patacrep>/songbook <patadata>/books/songbook_en.sb
>     <pdfreader> songbook_en.pdf

# Quick and dirty deb packages

Install `python-stdeb`, then:

>     python setup.py --command-packages=stdeb.command bdist_deb
>     sudo dpkg -i deb_dist/python-patacrep_<version>-1_all.deb

# Documentation

   http://www.patacrep.com/data/documents/doc_en.pdf

# Contact & Forums

* http://www.patacrep.com
* crep@team-on-fire.com
