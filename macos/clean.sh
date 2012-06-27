#!/bin/sh
#
echo "manually performs 'make clean'"
rm -rf *.aux *.d *.toc *.out *.log *.nav *.snm *.sbx *.sxd
echo "remove temporary covers"
rm -rf covers/
