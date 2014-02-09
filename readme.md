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

# Clone Patacrep repos

>     git clone git://github.com/crep4ever/songbook-core.git
>     git clone git://github.com/crep4ever/songbook-data.git
>     mv songbook-data songbook-core/songs

# Run

>     cd songbook-core
>     ./songbook.py -s <songbook_file.sb>
>     <pdfreader> <songbook_file.pdf>

Look for existing songbook files in ./books. For example:

>     ./songbook.py -s ./books/songbook_en.sb
>     evince songbook_en.pdf


# Documentation
   http://www.patacrep.com/data/documents/doc_en.pdf

# Contact & Forums
* http://www.patacrep.com
* crep@team-on-fire.com
