#!/bin/bash

# List of code pages to process
codepages=(
    437 500 500V1 850 851 852 855 856 857 858 860 861 862 863 864 865 866
    866NAV 869 874 904 1026 1046 1047 8859_1 8859_2 8859_3 8859_4 8859_5
    8859_6 8859_7 8859_8 8859_9 ANSI_X3.4-1968 ASCII BIG5 CP1250 CP1251
    CP1252 CP1253 CP1254 CP1255 CP1256 CP1257 CP1258 UTF-8
)

# Input file
input_file="1.txt"

# Iterate through each code page and convert
for codepage in "${codepages[@]}"; do
    iconv -f "$codepage" -t utf8 "$input_file"  
done


