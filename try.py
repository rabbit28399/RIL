import re
import en
from nltk.corpus import words
pattern = re.compile('_(VERB|VP)$')

with open('coba') as f:
    for line in f:
        ngram = line.split("\t")[0]
        grams = ngram.split()
        flag = False
        checker = False
        for gram in grams:
            if pattern.search(gram):
                gram_word = gram.split("_")[0]
                low = str("%s"%gram_word).lower()
                if low in words.words():
                    checker = True
                else:
                    print (low, "Tidak")
                break

        pp_list = []
        if checker:
            pp = en.verb.past_participle(low)
            pp_list.append(pp)
            print pp_list