#!/bin/sh

#Author: Romain Goffe
#Date: 13/10/2011
#Description: Build all the pdf on www.patacrep.com, increase their
#version and commit/tag the result

GREP="$GREP_OPTIONS"
export GREP_OPTIONS=""

#last volume
./utils/last-volume.sh
#english.sb
./utils/langbooks.sh english 
#french.sb
./utils/langbooks.sh french 

#increase version
RELEASE_TYPE=$1
VERSION=`grep "\"version\"" ./templates/patacrep.tmpl | sed -e 's/.*\"\([0-9]\+\)\.\([0-9]\+\)\.\?\([0-9]\+\)\?.*/export MAIN=\1\nexport MAJOR=\2\nexport MINOR=\3\n/'`
$VERSION

if [ $# -eq 1 ]
then
    echo "current version : $MAIN.$MAJOR.$MINOR"
    if [ $RELEASE_TYPE = "major" ];
    then
	MAJOR=$(($MAJOR+1))
	MINOR=0
    elif [ $RELEASE_TYPE = "minor" ];
    then
	MINOR=$(($MINOR+1))
    else
	echo "error: unrecognised release type"
    fi;
    echo "new version : $MAIN.$MAJOR.$MINOR"
    #update version field in tmpl files
    sed -i "s/\"[0-9]\+.[0-9]\+.[0-9]\+\"/\"$MAIN.$MAJOR.$MINOR\"/" templates/patacrep.tmpl
    sed -i "s/\"[0-9]\+.[0-9]\+.[0-9]\+\"/\"$MAIN.$MAJOR.$MINOR\"/" templates/ancient.tmpl
else
    echo "keeping release version"
fi;


#apply verification tools
#echo "emacs batch indentation in progress ..."
#./utils/indent.sh 2> /dev/null 
#echo "emacs batch indentation done !"
./utils/rules.py
./utils/resize-cover.py 
./utils/perms.sh

#build all songbooks
rm -f *.d 
make archive
make naheulbeuk.pdf 
make volume-1.pdf 
make volume-2.pdf 
make volume-3.pdf 
make volume-4.pdf 
make volume-5.pdf 
make english.pdf 
make french.pdf 
make songbook_fr.pdf 
make songbook_en.pdf 
make lyricbook_fr.pdf
make lyricbook_en.pdf
make clean

git status 

if [ $# -eq 1 ]
then
    ./utils/new-songs-list.sh | cat - NEWS > /tmp/out && mv -f /tmp/out NEWS
    echo "\nversion $MAIN.$MAJOR.$MINOR\n" | cat - NEWS > /tmp/out && mv -f /tmp/out NEWS
    git add templates/*.tmpl
    git add books/naheulbeuk.sb books/volume*.sb NEWS
    git commit -m "patacrep release version $MAIN.$MAJOR.$MINOR" 
    git tag "patacrep_$MAIN.$MAJOR.$MINOR"
fi

notify-send "Patacrep!" "Release $MAIN.$MAJOR.$MINOR generated" --icon=songbook-client

export GREP_OPTIONS="$GREP"
