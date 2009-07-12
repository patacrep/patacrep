#!/bin/sh
# Resize image if needed

for image in songs/*/*.jpg songs/*/*.png ; 
do
    SIZE=`identify $image | awk '{ print $3}' | sed 's/x/ /'`;
    XSIZE=`echo $SIZE | awk '{ print $1}'`;
    YSIZE=`echo $SIZE | awk '{ print $2}'`;

    if [ $((XSIZE)) -gt 128 ]
    then
	convert $image -resize 128x128 $image;
    elif [ $((YSIZE)) -gt 128 ]
    then
	convert $image -resize 128x128 $image;
    fi
done;