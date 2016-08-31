import re
import en
from google_ngram_downloader import readline_google_store
from nltk.corpus import words
all_records = readline_google_store(lang='eng', ngram_len=1, indices='a')
this_count = 0

pattern = re.compile('_(VERB|VP)$')
for (fname, url, records) in all_records:
    for r in records:
        ngram = r.ngram
        grams = ngram.split()
        flag = False
        checker = False
        for gram in grams:
            if pattern.search(gram):
                gram_word = gram.split("_")[0]
                low = str("%s" % gram_word).lower()
                if low in words.words():
                    flag = True
                    checker = True
                else:
                    print (low, "Not an English Word")
                break

        if flag:
            this_count += r.match_count
            print(gram_word)
            print(this_count)

        pp_list = []
        if checker:
            pp = en.verb.past_participle(low)
            pp_list.append(pp)
            print "PP LIST = ", pp_list
