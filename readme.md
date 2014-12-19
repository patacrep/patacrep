# Patacrep, a songbook compilation chain

This package provides a compilation toolchain that produce LaTeX
songbook using the LaTeX songs package. A new LaTeX document class is
provided to allow specific customisation and new command like embedded
guitar tabs or lilypond sheets.

Document are subject to the GNU GPLv2 except if another licence
is precised in the header.

# Python version

Patacrep is only compatible with Python > 3.3.

# Installation

## Using pip

As simple as

```
pip3 install patacrep
```

## For developement

Clone Patacrep repos:

```
git clone git://github.com/patacrep/patacrep.git
cd patacrep
pip3 install -r Requirements.txt
python3 setup.py install
```

# Run

```
songbook <songbook_file.sb>
<pdfreader> <songbook_file.pdf>
```

Look for existing songbook files in [patadata](http://github.com/patacrep/patadata)

# More informations

The full documentation is hosted by readthedoc, here : http://patacrep.readthedocs.org/

# Contact & Forums

* http://www.patacrep.com/forum
