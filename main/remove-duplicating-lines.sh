#!/bin/bash

# Check if input file is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

input_file=$1

# Remove duplicate lines from the input file
awk '!seen[$0]++' "$input_file" > "$input_file.tmp" && mv "$input_file.tmp" "$input_file"
