#!/bin/sh

#Author: Romain Goffe
#Date: 27/10/2010
#Description: apply typo rules depending on language for songs (.sg files)
#Commentary: to be merge with latex-preprocessing script

for song in $@; do
    echo $song
    if grep -q "selectlanguage{english}" $song
    then
	sed -i \
            -e 's/[\s]*?/?/g' \
            -e 's/[\s]*!/!/g' \
            -e 's/[\s]*:/:/g' \
            $song;
    elif grep -q "selectlanguage{french}" $song
    then
	sed -i \
            -e 's/\([^ ]\)?/\1 ?/g' \
            -e 's/\([^ ]\)!/\1 !/g' \
            -e '/\\gtab.*/ ! s/\([^ ]\):/\1 :/g' \
            $song;
    fi;
done; 
