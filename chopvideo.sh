#!/bin/bash
# echo $1 $2 $3

while getopts i:t:n:p:d: option
do
  case "${option}"
    in
    i) INPUTFILE=${OPTARG};;
    n) BASENAME=${OPTARG};;
    t) PIECEDURATION=${OPTARG};;
    p) PIECES=${OPTARG};;
    d) DESTINATION=${OPTARG};;
  esac
done

echo "--------------------"

# duration of the original clip in seconds
DURATION=$(ffprobe -i $INPUTFILE -show_entries format=duration -v quiet -of csv="p=0")

# segment time defaults to 1
if [ -z $PIECEDURATION ]; then
  if [ -z $PIECES ]; then
    PIECEDURATION=1
  else
    PIECEDURATION=`echo $DURATION/$PIECES | bc -l`
  fi
fi

if [[ -z $BASENAME ]]; then
  DATE=`date +%Y%m%d`
  BASENAME="Clip_$DATE"
fi

# if not a number of pieces is specified
if [ -z $PIECES ]; then
  PIECES=`echo $DURATION/$PIECEDURATION | bc`
fi

if [[ -z $DESTINATION ]]; then
  echo "Creating folder $BASENAME"
  echo "in $PWD"
  mkdir $BASENAME
  DESTINATION="$PWD/$BASENAME"
fi


echo "Chooping $INPUTFILE of $DURATION seconds"
echo "into $PIECES pieces of $PIECEDURATION seconds each"
echo
echo "Files will be named $BASENAME-XX"
echo "and placed in $DESTINATION/"
echo

i="0"
while [ $i -lt $PIECES ]
do
  n=$(printf "%03d" $i)
  PIECENAME="$BASENAME-$n.mov"
  echo "Creating $DESTINATION/$PIECENAME"
  cd $DESTINATION
  ffmpeg -ss $i -i $INPUTFILE -vcodec copy -t $PIECEDURATION $PIECENAME
  echo "done"
  i=$[$i+1]
done

echo "--------------------"
