#!/bin/sh

#Author: Romain Goffe
#Date: 14/11/2010
#Description: Generate an sb file containing all the songs in a given language

echo "Build songbook file for songs in english (1), french (2)"
read answer
case "$answer" in
    1)
        cat ./utils/header-en > english.sb
	for song in songs/*/*.sg; 
	do
	    if grep -q "selectlanguage{english}" $song
	    then
		echo "\t\""`ls $song | sed "s/songs\\///g"`"\"," >> english.sb
	    fi
	done
        #remove last coma before bracket
	truncate --size=-2 english.sb
	#close json values for key "songs"
	echo "]\n}" >> english.sb
      ;;
    2)
	cat ./utils/header-fr > french.sb
	for song in songs/*/*.sg; 
	do
	    if grep -q "selectlanguage{french}" $song
	    then
		echo "\t\""`ls $song | sed "s/songs\\///g"`"\"," >> french.sb
	    fi
	done
	#remove last coma before bracket
	truncate --size=-2 french.sb
	#close json values for key "songs"
	echo "]\n}" >> french.sb
	;;
esac
