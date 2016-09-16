#!/bin/bash
for var in "$@"
do
    python -u try5.py 3 "$var"
done

