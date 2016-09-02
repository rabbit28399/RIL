import pandas as pd
import csv
import en
from google_ngram_downloader import readline_google_store
from nltk.corpus import words
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

leng = raw_input("Enter N-grams Length: ")
ind = raw_input("Enter N-grams Indices: ")

fname, url, records = next(readline_google_store(lang='eng', ngram_len=leng, indices=ind))
dictVerb = {}
dictAdj = {}

f = open("VERB_Outfile_" + ind + "_" + leng + "-grams.csv", "w")
#h = open("ADJ_Outfile_" + ind + "_" + leng + "-grams.csv", "w")
w = csv.writer(f)
#x = csv.writer(h)

try:
    while True:
        line = next(records)
        if line is not None:
            if "_VERB" in line.ngram:
                print line.ngram, line.match_count
                if line.ngram in dictVerb:
                    dictVerb[line.ngram] += line.match_count
                else:
                    dictVerb[line.ngram] = line.match_count
            #if "_ADJ" in line.ngram:
                #print line.ngram, line.match_count
                #if line.ngram in dictAdj: dictAdj[line.ngram] += line.match_count
                #else: dictAdj[line.ngram] = line.match_count
        else:
            break
except StopIteration:
    pass

w.writerow(["Ngrams", "Past Participle", "Match_Count"])
for key, val in dictVerb.items():
    gram_word = key.split("_")[0].encode('utf-8')
    low = str("%s" % gram_word).lower()
    gram_lemma = lemmatizer.lemmatize(low, 'v')
    if gram_lemma in words.words():
        is_verb = en.is_verb(gram_lemma)
        if is_verb:
            try:
                past_part = en.verb.past_participle(gram_lemma)
                if en.is_adjective(past_part):
                    pp = past_part
                else:
                    pp = ''
                print pp
            except KeyError:
                print("KeyError encountered")
            w.writerow([gram_lemma, pp, val])
f.close()

df = pd.read_csv("VERB_Outfile_" + ind + "_" + leng + "-grams.csv", header = 0, index_col = ["Ngrams"])
dfnew = df.groupby(df.index).sum()
dfnew.to_csv("VERB_Result_" + ind + "_" + leng + "-grams.csv")

#x.writerow(["Ngrams", "Match_Count"])
#for key, val in dictAdj.items():
    #gram_word_adj = key.split("_")[0].encode('utf-8')
    #low_adj = str("%s" % gram_word_adj).lower()
    #gram_lemma_adj = lemmatizer.lemmatize(low_adj, 'v')
    #if gram_lemma_adj in words.words():
        #is_adj = en.is_adjective(gram_lemma_adj)
        #if is_adj:
            #x.writerow([gram_lemma_adj, val])
#h.close()
#df = pd.read_csv("ADJ_Outfile_" + ind + "_" + leng +"-grams.csv", header=0, index_col=["Ngrams"])
#dfnew = df.groupby(df.index).sum()
#dfnew.to_csv("ADJ_Result_" + ind + "_" + leng +"-grams.csv")
