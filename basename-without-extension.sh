#!/bin/bash
filename=$(basename -- "$1")
extension="${filename##*.}"
filename="${filename%.*}"
echo $filename
