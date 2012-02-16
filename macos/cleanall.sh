#!/bin/sh
#
echo "manually performs 'make cleanall'"
`dirname $0`/clean.sh
rm -rf *.pdf
