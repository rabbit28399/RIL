import pandas as pd
import csv
import en
import re
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
            if "_ADJ" in line.ngram:
                print line.ngram, line.match_count
                if line.ngram in dictAdj: dictAdj[line.ngram] += line.match_count
                else: dictAdj[line.ngram] = line.match_count
        else:
            break
except StopIteration:
    pass

w.writerow(["Ngrams", "Match_Count"])
for key, val in dictVerb.items():
    gram_word = key.split("_")[0].encode('utf-8')
    low = str("%s" % gram_word).lower()
    gram_lemma = lemmatizer.lemmatize(low, 'v')
    if gram_lemma in words.words():
        is_verb = en.is_verb(gram_lemma)
        if is_verb:
            w.writerow([gram_lemma, val])
f.close()

df = pd.read_csv("VERB_Outfile_" + ind + "_" + leng + "-grams.csv", header = 0, index_col = ["Ngrams"])
dfnew = df.groupby(df.index).sum()
dfnew.to_csv("VERB_Result_" + ind + "_" + leng + "-grams.csv")

sorted_list = {}
list1 = []
list2 = []
with open("VERB_Result_" + ind + "_" + leng + "-grams.csv", 'r+') as inf:
    for line in inf:
        reader = csv.reader(inf, delimiter=",")
        for i in reader:
            print i[0]
            try:
                past_part = en.verb.past_participle(i[0])
                for key, val in dictAdj.items():
                    key_b = key.lower().encode("utf-8")
                    if key_b == past_part + "_adj" :
                        print past_part, "Uyee", val
                        if i[0] in sorted_list:
                            sorted_list[i[0]] += val
                        else:
                            sorted_list[i[0]] = val
            except KeyError:
                print("Don't have past past_partarticiple")
                sorted_list[i[0]] = '0'
                past_part = '-'
            list1.append(past_part)
            list2.append(i[1])
inf.close()
print list1
print list2
print sorted_list

with open("VERB_Result_" + ind + "_" + leng + "-grams.csv", 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["VERB", "PP_ADJ_Count"])
    for key, value in sorted_list.items():
        writer.writerow([key, value])
csv_file.close()

df = pd.read_csv("VERB_Result_" + ind + "_" + leng + "-grams.csv", header = 0, index_col = ["VERB"])
df['Past_Participle'] = list1
df['VERB_COUNT'] = list2
df.to_csv("VERB_Result_" + ind + "_" + leng + "-grams.csv")


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
