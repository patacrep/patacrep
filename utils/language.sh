#!/bin/sh
echo "Choose langage: 1 (english), 2 (french), 3 (spanish)"
for song in songs/*/*.sg; do
    echo "Apply language to $song ?"
    read answer
    case "$answer" in
	1)
	    sed -i '1i\\\\selectlanguage{english}' $song
	    ;;
	2)
	    sed -i '1i\\\\selectlanguage{french}' $song
	    ;;
	3)
	    sed -i '1i\\\\selectlanguage{spanish}' $song
	    ;;
    esac
done; 
