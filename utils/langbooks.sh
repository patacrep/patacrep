#!/bin/sh

#Author: Romain Goffe
#Date: 14/11/2010
#Description: Generate an sb file containing all the songs in a given language

if [ $# -ne 1 ];
then
    echo "Usage: $0 LANG"
    exit 1
fi;

LANG=$1

if [ $LANG="english" -o $LANG="french" ];
then
    cp "./utils/header-$LANG" "$LANG.sb"
    grep "selectlanguage{$LANG}" songs/*/*.sg | sed 's|songs/\(.*\):.*|    \"\1\",|; $ s|,$|\n  ]\n}\n|' >> "$LANG.sb"
else
    echo "Error: $LANG is not a supported language"
    exit 2
fi;
