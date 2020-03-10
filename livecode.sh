#!/bin/bash
TEMPLATE=$1
FILENAME="livecoding-$(date +%Y%m%dT%H%M).scd"
if [ -z "$1" ]
then
    cp TEMPLATE FILENAME
fi
/Applications/nvim-osx64/bin/nvim $FILENAME
nvim $FILENAME
