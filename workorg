# !bin/bash
# NAME
#  workorg - create a folder and an .org file for a new job
# SYNOPSIS
#  workorg [-d DATE] [-c CONTACT] [-d DIRECTOR] [-f FILESPATH] [-D DEADLINE] clientname job...
# DESCRIPTION
#  workorg creates a folder and an .org file for a new job
# OPTIONS
#  -d DATE
#     Sets the date in %Y%m%d format.  Default to TODAY.
#  -c CONTACT
#     Sets the contact.
#  -D DIRECTOR
#     Sets the name of the director.
#  -f FILESPATH
#     Sets the path to the files being used.
#  -l DEADLINE
#     Sets the deadline in %Y%m%d format.
# EXAMPLES
# SEE ALSO
# BUGS
# AUTHOR
# COPYRIGHT
DATE=`date +%Y%m%d`
FILESPATH="[[./][files]]"

ARGS=()
while test $# -gt 0; do
    case "$1" in
        -d) shift
            DATE="${1}"
            shift
            ;;
        -c) shift
            CONTACT="${1}"
            shift 2
            ;;
        -D) shift
            DIRECTOR="${1}"
            shift 2
            ;;
        -f) shift
            FILESPATH="[[${1}][files]]"
            shift 2
            ;;
        -l) shift
            DEADLINE="${1}"
            shift 2
            ;;
        *)  ARGS+=("$1")
            shift
            ;;
    esac
done

CLIENT=`echo ${ARGS[0]} | awk '{print toupper}'`
CONCEPT=${ARGS[1]}
NAME="${CLIENT}-${DATE}-${CONCEPT}"
DIR="$(pwd)/${NAME}"
ORGFILE="${NAME}.org"

# # ----------------------------
# echo "
# dir: $DIR
# org: $ORGFILE
# contact: $CONTACT
# director: $DIRECTOR
# files: $FILESPATH
# deadline: $DEADLINE
# "
# exit 0
# # ----------------------

mkdir $DIR
cd $DIR
mkdir docs
echo "#+SETUPFILE: ../work-setup.org

* TODO
:PROPERTIES:
:client: $CLIENT
:concept: $CONCEPT
:contact:
:director:
:quantity: 0
:unitprice: 28
:files: [[./][files]]  
:deadline:
:comments:
:END:
" > $ORGFILE
open $ORGFILE
 
