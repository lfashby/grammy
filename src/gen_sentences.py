import json
import math
import random

with open("../json/unigrams.json", "r") as uni_source:
    uni_counts = json.load(uni_source)
with open("../json/log_bigram_probs.json", "r") as log_bigram_source:
    log_bigram_probs = json.load(log_bigram_source)

def calculate_prob_log_bigram_model(sentence):
    probabilities = []
    words = sentence.split(' ')
    for i in range(1, len(words)):
        prev = words[i - 1]
        curr = words[i]
        if prev in log_bigram_probs:
            if curr in log_bigram_probs[prev]:
                probabilities.append(log_bigram_probs[prev][curr])
                continue
        # Not sure what the recommended thing to do with logs is
        # when we encounter an out of vocabulary word.
        # Zero property of multiplication doesn't save us here.
        # return 0
    total_probability = math.exp(sum(probabilities))
    return total_probability


def build_sentence():
    # Working with the negative numbers and occasional 0.0 in log_bigram_probs.json
    # would be a nuisance.
    with open("../json/bigram_probs.json", "r") as bigram_source:
        bigram_probs = json.load(bigram_source)
    sentence = "<s> "
    alt_sentence = "<s> "
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
    alt_sentence += first_word
    input_word = first_word
    alt_input = first_word

    # Returns first following word that has a higher probability
    # value than randomly generated decimal between 0 and 1.
    # A bit more fun than just grabbing the highest probability following word.
    # Disregards the essentials of the 'word-to-word coherence'
    #  you'd build a bigram language model for in the first place.
    def grab_next_word(input_word):
        next_word = ""
        while not next_word:
            random_probability = random.random()
            for (word, prob) in bigram_probs[input_word].items():
                if prob >= random_probability:
                    next_word = word
                    break
        return next_word
    

    # This does function with some respect for the connections
    # between words established by a bigram language model.
    def grab_next_word_alt(sent, input_word):
        prospectives = []
        for variant in log_bigram_probs[input_word].keys():
            modified_sent = sent + variant
            prob = calculate_prob_log_bigram_model(modified_sent)
            prospectives.append([variant, prob])

        # Logic for grabbing random word with cumulative probability
        # calculated just for fun I guess.
        # random_selection = random.randint(0, len(prospectives) - 1)
        # to_return = prospectives[random_selection][0]
        
        largest = 0
        prev = []
        l_collection = []
        for pair in prospectives:
            num = round(math.exp(pair[1]), 10)
            if num == largest:
                l_collection.append(pair)
                continue
            if num > largest:
                largest = num
                prev.append(pair)
                l_collection.append(prev)
        # To avoid getting stuck in a loop of picking the highest prob each time.
        random_selection = random.randint(0, len(l_collection) - 1)
        to_return = prospectives[random_selection][0]
        return to_return

    # Grab new words until we hit </s>
    while True:
        input_word = grab_next_word(input_word)
        sentence += f" {input_word}"
        # Break if we reach end of sentence
        if input_word == "</s>":
            break

    # Can generate some very long sentences.
    while True:
            alt_input = grab_next_word_alt(alt_sentence, alt_input)
            alt_sentence += f" {alt_input}"
            if alt_input == "</s>":
                break
    return sentence, alt_sentence

sent, alt_sent = build_sentence()
print("Regular:", sent)
print("Cumulative:", alt_sent)
