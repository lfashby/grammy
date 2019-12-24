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


for (word, following_words_dict) in bigrams.items():
    for (following_word, count) in following_words_dict.items():
        # How many digits to round to a fairly arbitrary decision
        # Dividing the number of times the bigram occurs by number of times the preceding word occurs.
        # Same as dividing by the count of bigrams starting with preceding word.
        bigram_count = round(count/unigrams[word], 4)
        log_bigram_count = math.log(round(count/unigrams[word], 4)) # not sure if I should be providing a base here
        bigram_probs[word][following_word] = bigram_count
        log_bigram_probs[word][following_word] = log_bigram_count


with open("../json/bigram_probs.json", "w") as source:
    json_dict = json.dumps(bigram_probs, indent=4)
    source.write(json_dict)


with open("../json/log_bigram_probs.json", "w") as log_source:
    json_dict = json.dumps(log_bigram_probs, indent=4)
    log_source.write(json_dict)
