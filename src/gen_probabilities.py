import json
import math
from collections import defaultdict

# Creates json object of normalized bigram counts

with open("../json/unigrams.json", "r") as source:
    unigrams = json.load(source)

with open("../json/bigrams.json", "r") as source:
    bigrams = json.load(source)

# Word: { following word: probability }
bigram_probs = defaultdict(
    lambda:
        defaultdict(
            lambda: 0
        )
)

log_bigram_probs = defaultdict(
    lambda:
        defaultdict(
            lambda: 0
        )
)

for (word, preceding_words_dict) in bigrams.items():
    for (preceding_word, count) in preceding_words_dict.items():
        # How many digits to round to a fairly arbitrary decision
        bigram_count = round(count/unigrams[preceding_word], 4)
        log_bigram_count = math.log(round(count/unigrams[preceding_word], 4)) # not sure if I should be providing a base here
        bigram_probs[preceding_word][word] = bigram_count
        log_bigram_probs[preceding_word][word] = log_bigram_count

# In this object, each key is a unigram and it's associated value is
# a dict of words that follow it.
with open("../json/bigram_probs.json", "w") as source:
    json_dict = json.dumps(bigram_probs, indent=4)
    source.write(json_dict)

# In this object, each key is a unigram and it's associated value is
# a dict of words that precede it and their probability.
with open("../json/log_bigram_probs.json", "w") as log_source:
    json_dict = json.dumps(log_bigram_probs, indent=4)
    log_source.write(json_dict)
