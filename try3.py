import csv
import sys
from google_ngram_downloader import readline_google_store
from string import ascii_lowercase
import urllib, os

setVerbIdx = set()
out = open("index-verbs.csv", "w")
w = csv.writer(out)

for c in ascii_lowercase:

    f = open("Result-1gram/"+c+"-VERB-Result-1-grams.csv", "r")
    for line in f.readlines():
        verb = line.split(",")[0]
        setVerbIdx.add(verb[0:2])

for key in sorted(setVerbIdx):
    d = urllib.urlopen("http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"+key+".gz")
    x = int(d.info()['Content-Length'])
    if x <= 8589934592:
        w.writerow([key.encode('utf-8'), d.info()['Content-Length']])
        #os.system("nohup bash 3gram_man.sh"+key+"> nohup"+key+".out 2>&1 &")