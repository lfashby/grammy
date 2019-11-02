import json
from collections import defaultdict

# Creates json object of normalized bigram counts

with open("unigrams.json", "r") as source:
    unigrams = json.load(source)

with open("bigrams.json", "r") as source:
    bigrams = json.load(source)

# Unigram: { preceding words and probabilities }
bigrams_normalized_counts = defaultdict(
    lambda:
        defaultdict(
            lambda: 0
        )
)
# Unigram: { following words and probabilities }
bigrams_normalized_useful = defaultdict(
    lambda:
        defaultdict(
            lambda: 0
        )
)

for (word, preceding_words_dict) in bigrams.items():
    for (preceding_word, count) in preceding_words_dict.items():
        normalized_count = round(count/unigrams[preceding_word], 5)
        bigrams_normalized_counts[word][preceding_word] = normalized_count
        bigrams_normalized_useful[preceding_word][word] = normalized_count

# In this object, each key is a unigram and it's associated value is
# a dict of words that precede it and their probability.
with open("normalized_bigrams_prec.json", "w") as normalized_values_path:
    json_dict = json.dumps(bigrams_normalized_counts, indent=4)
    normalized_values_path.write(json_dict)

# In this object, each key is a unigram and it's associated value is
# a dict of words that follow it.
with open("normalized_bigrams.json", "w") as normalized_values_path:
    json_dict = json.dumps(bigrams_normalized_useful, indent=4)
    normalized_values_path.write(json_dict)
