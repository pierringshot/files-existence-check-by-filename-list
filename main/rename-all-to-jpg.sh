#!/system/bin/sh

# Input directory
input_directory="/storage/emulated/0/AutoShare/"

# Check if input directory exists
if [ ! -d "$input_directory" ]; then
    echo "Input directory $input_directory not found."
    exit 1
fi

# Change directory to input directory
cd "$input_directory"

# Rename all PNG files to JPG
find . -type f -iname "*.png" -exec sh -c 'mv "$1" "${1%.png}.jpg"' _ {} \;

# Rename all JPEG files to JPG
find . -type f -iname "*.jpeg" -exec sh -c 'mv "$1" "${1%.jpeg}.jpg"' _ {} \;

# Rename all WEBP files to JPG
find . -type f -iname "*.webp" -exec sh -c 'mv "$1" "${1%.webp}.jpg"' _ {} \;

echo "All image files in $input_directory have been converted to JPG format."
