#!/bin/sh

#Author: Romain Goffe
#Date: 13/10/2011
#Description: Build a tarball from the songbook git repo 

#Copy songbook directory
cd $HOME
cp -RH songbook songbook-$(date +%d)-$(date +%m)-$(date +%Y);

#Remove unecessary directories
cd songbook-$(date +%d)-$(date +%m)-$(date +%Y);
rm -rf perso/ ;
rm -rf data/ ;
rm -rf .git/ ;
rm -f .gitignore ;
rm -f utils/send.sh ;
rm -f books/tmp.sb books/default.sb
rm -f default*

#Clean tmp files
find . -name "*~" -or -name "#*#" -type f -exec rm -f {} \; 
make cleanall

#Tarball
cd $HOME
tar czvf songbook.tar.gz songbook-$(date +%d)-$(date +%m)-$(date +%Y)

#Remove copy
rm -rf songbook-$(date +%d)-$(date +%m)-$(date +%Y)/
