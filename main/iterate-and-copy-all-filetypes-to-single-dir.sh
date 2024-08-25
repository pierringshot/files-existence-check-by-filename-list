#!/bin/bash

destination_directory="/storage/emulated/0/importantFiles/ALLtools"

find . -type f \( -name "*.sh" -o -name "*.py" \) -exec cp {} "$destination_directory" \;
