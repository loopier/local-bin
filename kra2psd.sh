#!/usr/bin/env bash
set -euo pipefail

# batch convert all .kra files in path to .jpg
mkdir -p psds
for f in $@
do
    [ -d $f ] && continue
    filename=$(basename $f .kra)
    extension=$(echo ${f##*.})
    psdname="psds/${filename}.psd"
    krita $f --export --export-filename $psdname
    # echo $jpgname
    # echo $extension
done
