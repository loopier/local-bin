#!/usr/bin/env bash
set -euo pipefail

# batch convert all .kra files in path to .jpg
mkdir -p jpgs
for f in $@
do
    [ -d $f ] && continue
    filename=$(basename $f .kra)
    extension=$(echo ${f##*.})
    jpgname="jpgs/${filename}.jpg"
    krita $f --export --export-filename $jpgname
    # echo $jpgname
    # echo $extension
done
