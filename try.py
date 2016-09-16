import pandas as pd
import csv
import sys
import en
import nltk
import re
from google_ngram_downloader import readline_google_store
from nltk.corpus import words
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

ngramLen = sys.argv[1]
index = sys.argv[2]
fname, url, records = next(readline_google_store(lang="eng", ngram_len=ngramLen, indices=[index]))
dictVerbAdj = {}

x = open("Result-3gram/"+index + "-Outfile-" + ngramLen + "gram-verb-adj.csv", "w")
w = csv.writer(x)

try:
    while True:
        line = next(records)
        if line is not None:
            tokens = line.ngram.split(" ")
            if re.compile('VERB').search(tokens[0]) and re.compile('ADJ').search(tokens[-1]):
                print line.ngram.encode("utf-8"), line.match_count
                verb = tokens[0].split("_")[0]
                adj = tokens[-1].split("_")[0]
                if verb.isalpha() and adj.isalpha():
                    pattern = "-".join(tokens[1:-1])
                    if verb+":"+adj+":"+pattern in dictVerbAdj:
                        dictVerbAdj[verb+":"+adj+":"+pattern] += line.match_count
                    else:
                        dictVerbAdj[verb+":"+adj+":"+pattern] = line.match_count
        else:
            break

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

df = pd.read_csv("Result-3gram/" + index + "-Outfile-" + ngramLen + "gram-verb-adj.csv", header=0, index_col=["Verb : Adj : Pattern"])
dfnew = df.groupby(df.index).sum()
dfnew.to_csv("Result-3gram/"+index + "-Outfile-" + ngramLen + "gram-verb-adj.csv")

pat_newd = {}
patd = {}
with open("Result-3gram/"+index + "-Outfile-" + ngramLen + "gram-verb-adj.csv", 'r+') as inf:
    for line in inf:
        reader = csv.reader(inf, delimiter=",")
        for i in reader:
            pat = i[0].split(":")
            pat_newa = pat[2].split("_")[0]
            pat_new = pat[2].split("_")[-1]
            if pat_new:
                try:
                    if "det" not in pat_new and nltk.pos_tag([pat_new])[-1][-1] != "DT" and nltk.pos_tag([pat_new])[-1][-1] != "PRP$":
                        if nltk.pos_tag([pat_newa])[-1][-1] != "PRP$":
                            if pat[0] + ":" + pat[1] in patd:
                                if pat[0] + ":" + pat[1] + ":" + pat_new in pat_newd:
                                    pat_newd[pat[0] + ":" + pat[1] + ":" + pat_new] += int(i[1])
                                else:
                                    pat_newd[pat[0] + ":" + pat[1] + ":" + pat_new] = int(i[1])
                            else:
                                patd[pat[0] + ":" + pat[1]] = pat[0] + ":" + pat[1]
                                pat_newd[pat[0] + ":" + pat[1] + ":" + pat_new] = int(i[1])
                except ValueError:
                    pass
print patd
print pat_newd
inf.close()

with open("Result-3gram/"+index + "-Result-" + ngramLen + "gram-verb-adj.csv", 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Verb : Adj : Pattern", "Match_Count"])
    for key, value in sorted(pat_newd.items()):
        writer.writerow([key, value])
csv_file.close()
