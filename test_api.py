#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import en
from google_ngram_downloader import readline_google_store
from nltk.corpus import words
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
all_records = readline_google_store(lang='eng', ngram_len=1, indices='z')
this_ngram = "*"
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
                gram_word_unicode = gram_word.encode('utf-8')
                low = str("%s" % gram_word_unicode).lower()
                gram_lemma = lemmatizer.lemmatize(low, 'v')
                if gram_lemma in words.words():
                    flag = True
                    checker = True
                break

        if flag:
            if (gram_lemma == this_ngram):
                this_count += r.match_count
            else:
                print this_ngram, "\t", this_count
                this_ngram = gram_lemma
                this_count = r.match_count

        #pp_list = []
        #if checker:
            #pp = en.verb.past_participle(low)
            #pp_list.append(pp)
            #print "PP LIST = ", pp_list
