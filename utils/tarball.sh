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
rm -f crep.sgl ;
rm -f chords.tex ;
rm -f lilypond/*.ps ;
rm -f lilypond/*.pdf ;
rm -f utils/send.sh ;
rm -f utils/release.sh ;
rm -f utils/tarball.sh ;
rm -f tmp* 
rm -f default*
rm -f *.pdf 

#Clean tmp files
find . -name "*~" -type f -exec rm -f {} \; && find . -name "#*#" -type f -exec rm -f {} \;
make cleanall

#Tarball
cd $HOME
tar czvf songbook.tar.gz songbook-$(date +%d)-$(date +%m)-$(date +%Y)

#Remove copy
rm -rf songbook-$(date +%d)-$(date +%m)-$(date +%Y)/
