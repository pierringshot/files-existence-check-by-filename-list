#!/bin/bash

find . -type f \( -name "*.sh" -o -name "*.py" \) -exec sh -c 'echo "#{}"; cat {}' \; | tee scripts.txt
