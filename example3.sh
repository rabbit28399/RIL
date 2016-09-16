#!/bin/bash
for var in "$@"
do
    python -u 4grams.py 4 "$var"
done


