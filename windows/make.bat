Rem build tex file from songbook file
songbook.py --songbook=%1.sb --output=%1.tex

Rem 1st pdf compilation 
pdflatex %1.tex

Rem build indexes
songbook-makeindex.py %1_title.sxd > %1_title.sbx
songbook-makeindex.py %1_auth.sxd > %1_auth.sbx

Rem 2nd compilation to include indexes
pdflatex %1.tex
