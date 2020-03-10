# /bin/bash

KEYWORDS="TODO:|FIXME:|\?\?\?:|\!\!\!:"
find "${SRCROOT}" \( -name "*.h" -or -name "*.cpp" \) -print0 | xargs -0 egrep --with-filename --line-number --only-matching "($KEYWORDS).*\$" | perl -p -e "s/($KEYWORDS)/ warning: \$1/"
