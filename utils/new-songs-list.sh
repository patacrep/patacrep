#!/bin/sh
#
# Helper script to get the list of new songs added since the last version
# The output is supposed to be copy/pasted into the NEWS item.

if [ $# -eq 1 ]
then
    VERSION=$1
else
    # Get current version
    VERSION=`git tag | tail -n1`
fi

# Make new songs list by authors
git shortlog $VERSION..master | egrep '^([^ ].*|.*Add song.*)' | sed 's/Add song.*://' | sed 's/\.$//' | sed 's/ (.*)//' | sed 's/\s\s\s*/  /'
