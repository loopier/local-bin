# !/bin/bash

WORKINGDIR=""
OCTAVES=4
OCTAVE=3
NOTES=('A' 'A#' 'B' 'C' 'C#' 'D' 'D#' 'E' 'F' 'F#' 'G' 'G#')
NOTEINDEX=3

# Check arguments --------------------------# How it works
programname=$0

function usage {
    echo "usage: $programname [-m minsyllables] [-M maxsyllabs]"
    echo "  -n minsyllables   specify minimum number of syllabes"
    echo "  -M maxsyllables   specify maximum number of syllabes"
    exit 1
}

# Print errors
die() {
  printf '%s\n' "$1" >&2
  exit 1
}

while :; do
  case $1 in
    #  get path
    -i)
      if [[ -z "$2" ]]; then
        die "ERROR: '-i' requires a non-empty string option argument."
      else
        WORKINGDIR="$2"
        shift
      fi
      ;;
    *)               # Default case: No more options, so break out of the loop.
      if [[ $1 =~ ^-?[0-9]+$ ]]; then
        shift
      fi
      break
  esac

  shift
done
# End of check arguments --------------------------


printf "%s\n" "${NOTES[@]}"

echo "First note is ${NOTES[$NOTEINDEX]}$OCTAVE"

mkdir "$WORKINGDIR/notes"
SOURCEFILES="$WORKINGDIR/*.wav"
for f in $SOURCEFILES
do
  FILENAME="$WORKINGDIR/notes/${NOTES[$NOTEINDEX]}$OCTAVE.wav"
  cp $f $FILENAME
  echo "Copying $f to $FILENAME"
  NOTEINDEX=$(((NOTEINDEX+1) % ${#NOTES[@]}))
  if [[ $NOTEINDEX == 3 ]]; then
    OCTAVE=$((OCTAVE+1))
  fi
done
