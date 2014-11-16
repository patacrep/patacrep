Songbook Compilation Chain

# Description

This package provides a compilation toolchain that produce LaTeX
songbook using the LaTeX songs package. A new LaTeX document class is
provided to allow specific customisation and new command like embedded
guitar tabs or lilypond sheets.

Document are subject to the GNU GPLv2 except if another licence
is precised in the header.

# Python version

Patacrep is compatible with Python 3.

# Download

Clone Patacrep repos:

>     git clone git://github.com/patacrep/patacrep.git
>     git clone git://github.com/patacrep/patadata.git

# Installation from source

Make sure you have [pip](https://pip.pypa.io/en/latest/) installed, and then run

>     pip install -r Requirements.txt
>     python3 setup.py install

# Run

>     <patacrep>/songbook <songbook_file.sb>
>     <pdfreader> <songbook_file.pdf>

Look for existing songbook files in `<patadata>/books/`. For example:

>     <patacrep>/songbook <patadata>/books/songbook_en.sb
>     <pdfreader> songbook_en.pdf

# Documentation

- Compiled, but may be outdated: http://www.patacrep.com/data/documents/doc_en.pdf
- Documentation repository (to update the previous one): [patacrep-doc](http://github.com/patacrep/patacrep-doc)

# Contact & Forums

* http://www.patacrep.com
* crep@team-on-fire.com
