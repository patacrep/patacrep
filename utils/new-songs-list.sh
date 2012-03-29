#!/bin/sh
#
# Helper script to get the list of new songs added since the last version
# The output is supposed to be copy/pasted into the NEWS item.

GREP="$GREP_OPTIONS"
export GREP_OPTIONS=""

if [ $# -eq 1 ]
then
    VERSION=$1
else
    # Get current version
    VERSION=`git tag | grep patacrep | tail -n1`
fi

# Make new songs list by authors
git shortlog $VERSION..master | egrep '^([^ ].*|.*[aA]dd song.*)' | sed 's/[aA]dd song.//' | sed 's/\.$//' | sed 's/ (.*)//' | sed 's/\s\s\s*/  /'

export GREP_OPTIONS="$GREP"
