import re
dictVerbAdj = {}
line = "zz_VERB This_DET ancient_ADJ	1995	1	1"
ngram = line.split("\t")[0]
grams = ngram.split(" ")
if re.compile('VERB').search(grams[0]) and re.compile('ADJ').search(grams[-1]):
    print line
    verb = grams[0].split("_")[0]
    adj = grams[-1].split("_")[0]
    if verb.isalpha() and adj.isalpha():
        pattern = "-".join(grams[1:-1])
        if verb + ":" + adj + ":" + pattern in dictVerbAdj:
            dictVerbAdj[verb + ":" + adj + ":" + pattern] = verb + ":" + adj + ":" + pattern
        else:
            dictVerbAdj[verb + ":" + adj + ":" + pattern] = verb + "::::" + adj + ":" + pattern

print dictVerbAdj