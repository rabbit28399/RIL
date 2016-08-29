import re
from google_ngram_downloader import readline_google_store

all_records = readline_google_store(ngram_len=1, indices='a')

pattern = re.compile('_(VERB|VP)$')
for (fname, url, records) in all_records:
    for r in records:
        ngram=r.ngram
        grams=ngram.split()
        flag = False
        for gram in grams:
            if pattern.search(gram):
                flag = True
                break
        if flag: print(ngram)