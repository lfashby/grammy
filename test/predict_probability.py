import math
import json

# easy_sentence = "<s> HE KNELT DOWN AT HIS BED AS LONG AS HE COULD KNEEL </s>"
easy_sentence = "<s> PART OF THE RITUAL OF SEX IS THE USE OF MARIJUANA </s>"
# Guess it isn't so easy, 
# "<s> HE KNELT DOWN AT HIS BED AS LONG AS HE COULD KNEEL </s>"
# "KNELT"/"KNEEL" is not in the training data...
hard_sentence = "<s> SUCH WERE THE INCONGRUITIES OF THE SITUATION THAT THE VERY POLICE ASSIGNED TO CHECK UP ON ME WERE DRAFTED INTO DRIVING ME TO THE STRASBOURG HOSPITAL WHILE WORLD CITIZEN JEAN BABEL WAVED ADIEU FROM THE LINE </s>"


# Iterate through the sentence, assiging a probabliity
# that each word follows the next, add them together.

# Just for fun.
def calculate_prob_bigram_model(sentence):
    with open("../json/bigram_probs.json", "r") as bigram_source:
        bigram_probs = json.load(bigram_source)

    probabilities = []
    words = easy_sentence.split(' ')
    for i in range(1, len(words)):
        prev = words[i - 1]
        curr = words[i]
        if prev in bigram_probs:
            if curr in bigram_probs[prev]:
                probabilities.append(bigram_probs[prev][curr])
                continue
            print(f"{curr} never follows {prev} in training data.")
            continue
        print(f"{prev} does not occur in training data.")
        probabilities.append(0)
    # Python 3.8 has a math.prod() function which would be useful here.
    total_probability = 1
    for prob in probabilities:
        total_probability *= prob
    return total_probability

    
def calculate_prob_log_bigram_model(sentence):
    with open("../json/log_bigram_probs.json", "r") as bigram_source:
        bigram_probs = json.load(bigram_source)
    probabilities = []
    words = easy_sentence.split(' ')
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
        
    
        


print('NORMAL', calculate_prob_bigram_model(easy_sentence))
print('LOG', calculate_prob_log_bigram_model(easy_sentence))


def wb(sentence):
    with open("../json/log_bigram_probs.json") as bigram_source:
        bigram_probs = json.load(bigram_source)

    with open("../json/bigrams.json") as bigram_count_source:
        bigram_counts = json.load(bigram_count_source)

    probabilities = []
    words = easy_sentence.split(' ')
    for i in range(1, len(words)):
        prev = words[i - 1]
        curr = words[i]
        if prev in bigram_probs:
            if curr in bigram_probs[prev]:
                probabilities.append(bigram_probs[prev][curr])
            else:
                # We have no examples of curr following prev
                if prev == "<s>":
                    list_of_counts = 6111
                else:
                    list_of_counts = bigram_counts[prev].values()
                count_of_bigrams_for_prev_word: sum(list_of_counts)
                if prev == "<s>":
                    
                number_of_word_types = len(list_of_counts)
                probability = count_of_bigrams_for_prev_word / count_of_bigrams_for_prev_word + number_of_word_types
                probabilities.append(probability)
        # And what happens if prev is not in bigram_probs?
    print(probabilities)
    total_probability = math.exp(sum(probabilities))
    return total_probability

print("---------------------")
print("WB", wb(easy_sentence))