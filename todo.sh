# /bin/bash

path=$1

# default path is current directory
if [[ $# == 0 ]]; then
    path='.'
fi
# !!! TO DO - read multiple arguments

if [ -f ${path} ]; then
    echo "$path is a file"
elif [ -d ${path} ]; then
    echo "$path is a directory"
    echo "Parsing all files in the directory"
    path='*'

else
    echo "$path: No such file or directory"
    exit
fi
echo

# set line-break as the Internal Field Separator to
# get lines instead of words in 'grep'
defaultIFS=$IFS
IFS=$'\n'

# get lines where there is an instance of '!!!' and 
# the following 2 lines
todolist=($(grep -nr -A 2 '!!!' $path))

echo "${#todolist[@]} elements have been found"
echo

# print lines
for (( i = 0; i < ${#todolist[@]}; i++ )); do
    hasslashes=(${todolist[${i}]})
    echo "$hasslashes"
    # check if it has slashes
    if [[ ! "$hasslashes" =~ '//' ]] ; then  
        echo
        echo
    fi
done
echo

# restore default IFS
IFS=$defaultIFS


