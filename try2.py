import csv
import pandas as pd
from google_ngram_downloader import readline_google_store
import en
fname, url, records = next(readline_google_store(lang='eng', ngram_len=1, indices='z'))
h = open("VERB_Result_z_1-grams.csv", 'r+')
x = csv.writer(h)
dictAdj = {}
try:
    while True:
        line = next(records)
        if line is not None:
            if "_ADJ" in line.ngram:
                print line.ngram, line.match_count
                if line.ngram in dictAdj: dictAdj[line.ngram] += line.match_count
                else: dictAdj[line.ngram] = line.match_count
        else:
            break
except StopIteration:
    pass

sorted_list = {}
list1 = []
list2 = []
with h as inf:
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
                print("Don't have past ppast_partarticiple")
                sorted_list[i[0]] = '0'
                past_part = '-'
            list1.append(past_part)
            list2.append(i[1])
inf.close()
print list1
print list2
print sorted_list

with open("VERB_Result_z_1-grams.csv", 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["VERB", "PP_ADJ_Count"])
    for key, value in sorted_list.items():
        writer.writerow([key, value])
csv_file.close()

df = pd.read_csv("VERB_Result_z_1-grams.csv", header = 0, index_col = ["VERB"])
df['Past_Participle'] = list1
df['VERB_COUNT'] = list2
df.to_csv("VERB_Result_z_1-grams.csv")