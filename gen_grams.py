import json
from collections import defaultdict

# Creates json object of unigrams/bigrams and counts in refined_text.txt

unigram_dict = {}
bigram_dict = {}

bigram_dict = defaultdict(
    lambda:
        defaultdict(
            lambda: 0
        )
)

with open("refined_text.txt", "r") as text:
    for sentence in text:
        # Seperate into words, remove "\n"
        sentence = sentence.rstrip("\n")
        words = sentence.split(' ')
        for i in range(len(words)):
            # Add to or increment unigram dict
            if words[i] in unigram_dict:
                unigram_dict[words[i]] += 1
            else:
                unigram_dict[words[i]] = 1
            # Add to or increment bigram dict
            if i > 0:
                if words[i - 1] in bigram_dict[words[i]]:
                    bigram_dict[words[i]][words[i - 1]] += 1
                else:
                    bigram_dict[words[i]][words[i - 1]] = 1

# Export dicts to json
with open("unigrams.json", "w") as uni_file:
    json_dict = json.dumps(unigram_dict, indent=4)
    uni_file.write(json_dict)

with open("bigrams.json", "w") as bi_file:
    json_dict = json.dumps(bigram_dict, indent=4)
    bi_file.write(json_dict)
