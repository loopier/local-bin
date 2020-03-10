# Archives a story-board
# Deletes PSD files and 'doc' folder
# 
# @param {String} $1   destination directory where storyboard will be archived

# get name for messages
name=${PWD##*/}
parentDir="$(dirname `pwd`)"
destinationDir=${1-$parentDir}

echo "Archiving $name to $parentDir"

foldersToDelete=`ls */ | wc -l`
echo "Found $foldersToDelete folders"

numOfPsd=`ls *.psd | wc -l`
numOfPsdCaps=`ls *.PSD | wc -l`
numOfPsd=`expr $numOfPsd + $numOfPsdCaps`
echo "Found $numOfPsd PSD files"

echo "Removing PSD files..."
rm *.psd
rm *.PSD
echo "Done"
echo "Removing directories..."
rm -r */
echo "Done"

echo "Moving to $destinationDir..."
mv `pwd` $destinationDir

