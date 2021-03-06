import math
import json

easy_sentence = "<s> PART OF THE RITUAL OF SEX IS THE USE OF MARIJUANA </s>"
# easy_sentence = "<s> MY FATHER HAD NONE </s>"
# Iterate through the sentence, assiging a probabliity
# that each word follows the next, add them together.

# Just for fun.
def calculate_prob_bigram_model(sentence):
    with open("../json/bigram_probs.json", "r") as bigram_source:
        bigram_probs = json.load(bigram_source)
    probabilities = []
    words = sentence.split(' ')
    for i in range(1, len(words)):
        prev = words[i - 1]
        curr = words[i]
        if prev in bigram_probs:
            if curr in bigram_probs[prev]:
                probabilities.append(bigram_probs[prev][curr])
                continue
            print(f"{curr} never follows {prev} in training data.")
            probabilities.append(0)
            continue
        print(f"{prev} does not occur in training data.")
        probabilities.append(0)
    # Python 3.8 has a math.prod() function which would be useful here.
    total_probability = 1
    for prob in probabilities:
        total_probability = total_probability * prob
    return total_probability


def calculate_prob_laplace(sentence):
    with open("../json/log_bigram_probs.json", "r") as bigram_source:
        log_bigram_probs = json.load(bigram_source)
    with open("../json/unigrams.json", "r") as u_source:
        uni_counts = json.load(u_source)
    
    probabilities = []
    words = sentence.split(" ")
    for i in range(1, len(words)):
        prev = words[i - 1]
        curr = words[i]
        if prev in log_bigram_probs:
            if curr in log_bigram_probs[prev]:
                probabilities.append(log_bigram_probs[prev][curr])
                continue
            else:
                new_prob = math.log(1 / (uni_counts[prev] + len(uni_counts)))
                print("Running laplace smooting")
                probabilities.append(new_prob)
    total_probability = math.exp(sum(probabilities))
    return total_probability



def calculate_prob_log_bigram_model(sentence):
    with open("../json/log_bigram_probs.json", "r") as bigram_source:
        bigram_probs = json.load(bigram_source)
    probabilities = []
    words = sentence.split(' ')
    for i in range(1, len(words)):
        prev = words[i - 1]
        curr = words[i]
        if prev in bigram_probs:
            if curr in bigram_probs[prev]:
                probabilities.append(bigram_probs[prev][curr])
                continue
        # Not sure what the recommended thing to do with logs is
        # when we encounter an out of vocabulary word.
        # Zero property of multiplication doesn't save us here.
        # return 0
    total_probability = math.exp(sum(probabilities))
    return total_probability


normal = calculate_prob_bigram_model(easy_sentence)
log = calculate_prob_log_bigram_model(easy_sentence)


def wb(sentence):
    with open("../json/log_bigram_probs.json") as bigram_source:
        bigram_probs = json.load(bigram_source)

    with open("../json/bigrams.json") as bigram_count_source:
        bigram_counts = json.load(bigram_count_source)

    probabilities = []
    words = sentence.split(' ')
    for i in range(1, len(words)):
        prev = words[i - 1]
        curr = words[i]
        if prev in bigram_probs:
            if curr in bigram_probs[prev]:
                probabilities.append(bigram_probs[prev][curr])
            else:
                # We have no examples of curr following prev
                list_of_counts = bigram_counts[prev].values()
                count_of_bigrams_for_prev_word = sum(list_of_counts)
                number_of_word_types = len(list_of_counts)
                # Total count of bigrams for prev word - same as unigram count 
                # / 
                # total count of bigrams for prev word + number of different bigrams that occur after prev word.
                probability = math.log(round(
                    (
                        count_of_bigrams_for_prev_word / (count_of_bigrams_for_prev_word + number_of_word_types)
                    ),
                    4)
                )
                probabilities.append(probability)
    print(probabilities)
    total_probability = math.exp(sum(probabilities))
    return total_probability


wb_prob = wb(easy_sentence)
lp_prob = calculate_prob_laplace(easy_sentence)
print("Normal EXPO", normal)
print("Normal", "{:.14f}".format(normal))
print("Log", "{:.14f}".format(log))
print("WB EXPO", wb_prob)
print("WB", "{:.14f}".format(wb_prob))
print("LAPLACE EXPO", lp_prob)
print("LAPLACE", "{:.14f}".format(lp_prob))
print(wb_prob > lp_prob)