# lc - list directories and the number of elements it contains
find ${1:-"."} -type d -maxdepth 1 -print0 | while read -d '' -r dir; do
    files=("$dir"/*)
    printf "%s (%d)\n" "$dir" "${#files[@]}"
done
