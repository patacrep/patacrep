#!/bin/sh
#
echo "build tex file from songbook file"
./songbook.py --songbook=books/$1.sb --output=$1.tex

echo "first pdf compilation" 
/usr/texbin/pdflatex $1.tex

echo "build indexes"
./songbook-makeindex.py $1_title.sxd > $1_title.sbx
./songbook-makeindex.py $1_auth.sxd > $1_auth.sbx

echo "second compilation to include indexes"
/usr/texbin/pdflatex $1.tex
