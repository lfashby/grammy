import json
import random

# TODO - FIX THIS NOW THAT FILES HAVE CHANGED AND PREC NO LONGER EXISTS

with open("../json/unigrams.json", "r") as uni_source:
    uni_counts = json.load(uni_source)


def build_sentence():
    # Working with the negative numbers and occasional 0.0 in log_bigram_probs.json
    # would be annoying.
    with open("../json/bigram_probs.json", "r") as bigram_source:
        bigram_probs = json.load(bigram_source)
    sentence = "<s> "
    # Grab random starting word from <s>
    starter_dict = bigram_probs["<s>"]
    random_val = random.randint(0, len(starter_dict))
    i = 0
    for key in starter_dict:
        if i == random_val:
            first_word = key
            break
        i += 1

    sentence += first_word
    input_word = first_word

    # Returns first following word that has a higher probability
    # value than randomly generated decimal between 0 and 1.
    def grab_next_word(input_word):
        next_word = ""
        while not next_word:
            random_probability = random.random() # a bit more fun than just grabbing the highest probability following word.
            for (word, prob) in bigram_probs[input_word].items():
                if prob >= random_probability:
                    next_word = word
                    break
        return next_word
    
    # Grab new words until we hit </s>
    while True:
        input_word = grab_next_word(input_word)
        sentence += f" {input_word}"
        # Break if we reach end of sentence
        if input_word == "</s>":
            break
    return (first_word, sentence)


first_word, forward_sentence = build_sentence()
print("Selected first word:", first_word)
print("Forward generated sentence:", forward_sentence)
