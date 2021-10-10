#!/usr/bin/env bash
set -euo pipefail

POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -f|--filename)
      FILENAME="$2"
      shift # past argument
      shift # past value
      ;;
    -o|--output)
      OUTPUT="$2"
      shift # past argument
      shift # past value
      ;;
    -s|--scale)
      SCALE="$2"
      shift # past argument
      shift # past value
      ;;
    -t|--tiles)
      COLS_ROWS="$2"
      shift # past argument
      shift # past value
      ;;
    *)    # unknown option
      POSITIONAL+=("$1") # save it in an array for later
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL[@]}" # restore positional parameters

if [ ! -v FILENAME ] || [ ! -v SCALE ] || [ ! -v COLS_ROWS ]
then
    echo "usage: spritesheet -f [FILENAME] -s [WIDTH:HEIGHT] -t [COLSxROWS]"
    exit 0
fi

if [ ! -v OUTPUT ]
then
    OUTPUT=$FILENAME-$(echo $SCALE | sed -r 's/:/x/').png
fi

FILENAME=$FILENAME.%04d.png

echo "FILE NAME  = ${FILENAME}"
echo "SCALE      = ${SCALE}"
echo "TILES      = ${COLS_ROWS}"
echo "OUTPUT      = ${OUTPUT}"

ffmpeg -i $FILENAME -filter_complex scale=$SCALE,tile=$COLS_ROWS $OUTPUT
