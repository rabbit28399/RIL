import pandas as pd
import glob
import csv
import sys
ind = sys.argv[1]
with open("Result-"+ind+"gram-copy/FINAL-RESULT.csv",'wb') as fout:
    wout = csv.writer(fout,delimiter=',')
    wout.writerow(["VERB", "PP_ADJ_Count", "Past_Participle", "VERB_COUNT"])
    interesting_files = glob.glob("Result-"+ind+"gram-copy/*.csv")

    for filename in interesting_files :
        if 'VERB' in filename:
            with open(filename,'rb') as fin:
                fin.next()
                for line in csv.reader(fin,delimiter=','):
                    if '0' not in line:
                        wout.writerow(line)
                        print line[0]

fout.close()
df = pd.read_csv("Result-"+ind+"gram-copy/FINAL-RESULT.csv", index_col = ["VERB"])
value = df['PP_ADJ_Count']*df['VERB_COUNT']
df['Total_Count'] = value
df.to_csv("Result-"+ind+"gram-copy/FINAL-RESULT.csv")

df = pd.read_csv("Result-"+ind+"gram-copy/FINAL-RESULT.csv", index_col = ["VERB"])
test = df.sort_values('Total_Count', ascending=False)
test.to_csv("Result-"+ind+"gram-copy/FINAL-RESULT.csv")