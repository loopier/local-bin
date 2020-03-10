#!/bin/bash
#script to convert all .PSD files in the current directory to .JPG

for ff in *.psd;
do
filename=$(basename $ff)
extension=${filename##*.}
filename=${filename%.*}
convert ${ff} ${filename}.jpg
done