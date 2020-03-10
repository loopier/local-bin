# !/bin/bash
# Convert movies to animated gifs
FILE=$1
OUTPUTFILENAME="$(basename-without-extension.sh $FILE).gif"
echo "Generating color palette..."
# Generate palette
PALETTE="/tmp/palette.png"
ffmpeg -i $FILE -vf palettegen $PALETTE
echo "Done genrating palette"
echo "Converting $FILE to animated gif..."
ffmpeg -i $FILE -i $PALETTE -lavfi paletteuse $OUTPUTFILENAME
rm $PALETTE
