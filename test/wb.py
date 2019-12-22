
import json

# with open("../json/unigrams.json", "r") as uni_source:
#     uni_counts = json.load(uni_source)

with open("../json/normalized_bigrams.json") as bigram_source:
    bigram_object = json.load(bigram_source)


# Say we are given a word:
prev_word = ""
next_word = ""
if prev_word in bigram_object:
    # But we have no examples of next_word following prev_word
    if next_word not in bigram_object[prev_word]:
        count_of_bigrams_for_prev_word = len(bigram_object[prev_word])
        num_of_words_seen_more_than_once_after_prev_word = 0
        for count in bigram_object[prev_word].values():
            if count >= 1:
                num_of_words_seen_more_than_once_after_prev_word += 1
        # That's it?
        wb = count_of_bigrams_for_prev_word / count_of_bigrams_for_prev_word + num_of_words_seen_more_than_once_after_prev_word