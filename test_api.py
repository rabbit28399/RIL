import re
import en
from google_ngram_downloader import readline_google_store
all_records = readline_google_store(ngram_len=1, indices =  'z')

pattern = re.compile('_(VERB|VP)$')
for (fname, url, records) in all_records:
    for r in records:
        ngram=r.ngram
        grams=ngram.split()
        flag = False
        for gram in grams:
            if pattern.search(gram):
                flag = True
                pp_list = []
                gram_word = ngram.split("_")[0]
                #pp = en.verb.past_participle('"%s"'%gram_word)
                #pp_list.append(pp)
                #print pp_list
                break
        if flag: print(ngram)