#!/bin/sh
#
#Author: Romain Goffe and Alexandre Dupas
#Date: 27/10/2010
#Description: fix typographic mistakes, some depending on language

FILES=songs/*/*.sg

if [ $# -gt 0 ] ; then
    FILES=$@
fi

# remove trailing space and double space
sed -i \
    -e 's/\s*$//g' \
    -e 's/[,\.]$//g' \
    -e '/\s*%/! s/\([^ ]\)\s\+/\1 /g' \
    $FILES

# formating rules depending on language
for song in $FILES;
do
    if grep -q "selectlanguage{english}" $song
    then
	sed -i \
            -e 's/\s*?/?/g' \
            -e 's/\s*!/!/g' \
            -e 's/\s*:/:/g' \
            $song
    elif grep -q "selectlanguage{french}" $song
    then
	sed -i \
            -e 's/\([^ ]\)?/\1 ?/g' \
            -e 's/\([^ ]\)!/\1 !/g' \
            -e 's/\([^ ]\)!/\1 !/g' \
            -e 's/``/{\\og}/g' \
            -e "s/''/{\\\\fg}/g" \
            -e '/\\gtab.*/ ! s/\([^ ]\):/\1 :/g' \
            $song
    fi
done
