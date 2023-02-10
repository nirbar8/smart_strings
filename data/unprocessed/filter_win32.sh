#!/bin/bash

# This script is used to filter only the windows 32 bit PE and remove the rest of the files
# The directory is passed as an argument to the script

# Check if the directory is passed as an argument
if [ $# -eq 0 ]
then
    echo "No arguments supplied"
    exit 1
fi

# Check if the directory exists
if [ ! -d "$1" ]
then
    echo "Directory does not exist"
    exit 1
fi

# iterate through the directory and filter the files
for file in $1/*
do
    # if not a PE32 executable, remove the file
    if ! file $file | grep -q "PE32 executable"
    then
        rm $file
    fi
done

