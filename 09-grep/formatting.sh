#!/bin/bash
dos2unix text.txt
sed -i 's/[ \t]*$//' text.txt  # Remove trailing spaces

