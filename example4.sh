#!/bin/bash
for var in "$@"
do
    python -u 5grams.py 5 "$var"
done


