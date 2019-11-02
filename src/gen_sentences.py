import json
import random

with open("../json/unigrams.json", "r") as uni_source:
    uni_counts = json.load(uni_source)


# Uses gen_senenteces_prec.json to build sentence backwards.
def build_sentence_backwards():
    with open("../json/normalized_bigrams_prec.json", "r") as prec_source:
        bigram_prec_probs = json.load(prec_source)

    # Helper function for building sentence backward
    # Grabs first highest probablity preceding word
    # (Kind of boring thing to do)
    def grab_preceding_word(input_word):
        highest_prob = 0
        for (n_minus_1, prob) in bigram_prec_probs[input_word].items():
            if prob > highest_prob:
                highest_prob = prob
                preceding_word = n_minus_1
        return preceding_word

    # Grab random ending word from uni_counts
    # (probably quicker than iterating through bigram_prec_probs)
    # (Could grab random word from </s> in bigram_prec_probs each time)
    random_val = random.randint(0, len(uni_counts))
    i = 0
    for key in uni_counts:
        if i == random_val:
            selected_last_word = key
            break
        i += 1

    # Build from ending word to start
    # grabbing first highest probablity preceding word each time
    sentence = selected_last_word
    input_word = selected_last_word
    random_length = random.randint(4, 13)
    for _ in range(random_length):
        input_word = grab_preceding_word(input_word)
        sentence = input_word + ' ' + sentence
        # Break if we reach beginning of sentence
        if input_word == "<s>":
            break
    return (selected_last_word, sentence)


def build_sentence_forwards():
    with open("../json/normalized_bigrams.json", "r") as bigram_source:
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

    def grab_next_word(input_word):
        next_word = ""
        while not next_word:
            random_probability = random.random()
            for (word, prob) in bigram_probs[input_word].items():
                if prob >= random_probability:
                    next_word = word
                    break
        return next_word
    
    # Grab new words until we hit </s> or random sentence length
    random_length = random.randint(4, 13)
    for _ in range(random_length):
        input_word = grab_next_word(input_word)
        sentence += f" {input_word}"
        # Break if we reach beginning of sentence
        if input_word == "</s>":
            break
    return (first_word, sentence)


last_word, backwards_sentence = build_sentence_backwards()
print("Selected last word:", last_word)
print("Backward generated sentence:", backwards_sentence)
print("--------------------")
first_word, forward_sentence = build_sentence_forwards()
print("Selected first word:", first_word)
print("Forward generated sentence:", forward_sentence)
