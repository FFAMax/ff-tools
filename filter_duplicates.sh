#!/bin/bash

folder_a="a"
folder_b="b"

# Create a temporary file to store unique lines from folder a
temp_file_a=$(mktemp)
for file_a in "$folder_a"/*.txt; do
  cat "$file_a" >> "$temp_file_a"
done
sort -u "$temp_file_a" -o "$temp_file_a"

# Iterate through files in folder b and remove lines present in folder a's files
for file_b in "$folder_b"/*.txt; do
  temp_file_b=$(mktemp)
  grep -Fvxf "$temp_file_a" "$file_b" > "$temp_file_b"
  mv "$temp_file_b" "$file_b"
done

# Remove the temporary file for folder a
rm "$temp_file_a"

exit 0

# cat a/*
123
234
345
456
567
678
789
890

# cat b/*
567
0123
1234
# bash filter_duplicates.sh
# cat a/*
123
234
345
456
567
678
789
890

# cat b/*
0123
1234
