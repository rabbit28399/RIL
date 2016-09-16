#!/bin/bash
for var in "$@"
do
    python -u test_api.py 1 "$var"
done
