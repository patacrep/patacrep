#!/bin/sh

#Author: Romain Goffe
#Date: 07/03/2012
#Description: Check directories and files permissions

chmod 755 songs/*
chmod 644 songs/*/*.*
chmod 644 lilypond/*.ly

exit 0