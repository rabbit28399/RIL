import nltk
import pandas as pd
import csv
import sys

index = sys.argv[1]
df = pd.read_csv("Result-3gram/Result-3gram-z/"+index+"-Outfile-3gram-verb-adj.csv", header = 0, index_col = ["Verb : Adj : Pattern"])
dfnew = df.groupby(df.index).sum()
dfnew.to_csv("Result-3gram/Result-3gram-z/"+index+"-Outfile-3gram-verb-adj.csv")

pat_newd = {}
patd = {}
with open("Result-3gram/Result-3gram-z/"+index+"-Outfile-3gram-verb-adj.csv", 'r+') as inf:
    for line in inf:
        reader = csv.reader(inf, delimiter=",")
        for i in reader:
            pat = i[0].split(":")
            pat_newa = pat[2].split("_")[0]
            pat_new = pat[2].split("_")[-1]
            if pat_new:
                try :
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
                except ValueError : pass

print patd
print pat_newd
inf.close()

with open("Result-3gram/Result-3gram-z/Result/"+index+"-Result-3gram-verb-adj.csv", 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Verb : Adj : Pattern", "Match_Count"])
    for key, value in sorted(pat_newd.items()):
        writer.writerow([key, value])
csv_file.close()