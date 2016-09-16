import pandas as pd
import csv
import sys
import en
from google_ngram_downloader import readline_google_store
from nltk.corpus import words
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

ngramLen = sys.argv[1]
index = sys.argv[2]
fname, url, records = next(readline_google_store(lang = "eng", ngram_len=ngramLen, indices=[index]))
dictVerbAdj = {}

x = open("Result-5gram/"+index + "-Outfile-" + ngramLen + "gram-verb-adj.csv", "w")
w = csv.writer(x)

try:
    while True:
        line = next(records)
        if line is not None:
            #process line, check if first token contains _VERB, last token contains _ADJ, print to file with frequencies, etc.
            print line.ngram.encode("utf-8"), line.match_count
            tokens = line.ngram.split(" ")
            if "_VERB" in tokens[0] and "_ADJ" in tokens[-1]:
                verb = tokens[0].split("_")[0] #aa_VERB
                adj = tokens[-1].split("_")[0] #zz_ADJ
                #check if 'verb' is really a verb and 'adj' is really an adjective, get verb's infinitive, etc.
                if verb.isalpha() and adj.isalpha():
                    pattern = "|".join(tokens[1:-1])
                    if verb+":"+adj+":"+pattern in dictVerbAdj: dictVerbAdj[verb+":"+adj+":"+pattern] += line.match_count
                    else: dictVerbAdj[verb+":"+adj+":"+pattern] = line.match_count
        else: break

except StopIteration:
    pass

w.writerow(["Verb : Adj : Pattern", "Match_Count"])
for key, val in dictVerbAdj.items():
    low = str("%s" % key.encode("utf-8")).lower()
    sp = low.split(":")
    vb_lemma = lemmatizer.lemmatize(sp[0], 'v')
    pt = ":".join(sp[1:])
    if vb_lemma in words.words():
        is_verb = en.is_verb(vb_lemma)
        if is_verb:
            w.writerow([vb_lemma + ":" + pt, val])
x.close()

df = pd.read_csv("Result-5gram/"+index + "-Outfile-" + ngramLen + "gram-verb-adj.csv", header = 0, index_col = ["Verb : Adj : Pattern"])
dfnew = df.groupby(df.index).sum()
dfnew.to_csv("Result-5gram/"+index + "-Outfile-" + ngramLen + "gram-verb-adj.csv")

pat_newd = {}
patd = {}
with open("Result-5gram/"+index + "-Outfile-" + ngramLen + "gram-verb-adj.csv", 'r+') as inf:
    for line in inf:
        reader = csv.reader(inf, delimiter=",")
        for i in reader:
            pat = i[0].split(":")
            pat_new = pat[2].split("|")
            pat_new2 = pat_new[0].split("_")[-1]
            pat_new3 = pat_new[1].split("_")[-1]
            pat_new4 = pat_new[2].split("_")[-1]
            if pat_new2 and pat_new3 and pat_new4:
                if pat[0] + ":" + pat[1] in patd:
                    if pat[0] + ":" + pat[1] + ":" + pat_new2 + "-" + pat_new3 + "-" + pat_new4 in pat_newd:
                        pat_newd[pat[0] + ":" + pat[1] + ":" + pat_new2 + "-" + pat_new3 + "-" + pat_new4] += int(i[1])
                    else:
                        pat_newd[pat[0] + ":" + pat[1] + ":" + pat_new2 + "-" + pat_new3 + "-" + pat_new4] = int(i[1])
                else:
                    patd[pat[0] + ":" + pat[1]] = pat[0] + ":" + pat[1]
                    pat_newd[pat[0] + ":" + pat[1] + ":" + pat_new2 + "-" + pat_new3 + "-" + pat_new4] = int(i[1])
print patd
print pat_newd
inf.close()

with open("Result-5gram/"+index + "-Result-" + ngramLen + "gram-verb-adj.csv", 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Verb : Adj : Pattern", "Match_Count"])
    for key, value in sorted(pat_newd.items()):
        writer.writerow([key, value])
csv_file.close()