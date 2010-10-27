#!/bin/sh

#Author: Romain Goffe
#Date: 27/10/2010
#Description: apply typo rules depending on language for songs (.sg files)
#Commentary: to be merge with latex-preprocessing script

for song in songs/*/*.sg; do
    if grep -q "selectlanguage{english}" $song
    then
	sed -i "s/ ?/?/g" $song;
	sed -i "s/ !/!/g" $song;
	sed -i "s/ :/:/g" $song;
    fi;
    if grep -q "selectlanguage{french}" $song
    then
	sed -i "s/?/ ?/g" $song;
	sed -i "s/  ?/ ?/g" $song;
	sed -i "s/!/ !/g" $song;
	sed -i "s/  !/ !/g" $song;
	sed -i "s/:/ :/g" $song;
	sed -i "s/  :/ :/g" $song;
    fi;
done; 
