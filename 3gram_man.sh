#!/bin/bash
for var in "$@"
do
        wget "http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-$var.gz"
        gunzip "googlebooks-eng-all-3gram-20120701-$var.gz"
        python -u 3gram_man.py 3 "$var"
done

