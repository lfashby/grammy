import math
import random
from nltk.corpus import brown

# A very quick and imperfect way of getting
# the sorts of sentences I want to work with.

sentences = brown.sents(categories="belles_lettres")
beginning = "<s>"
end = "</s>\n"
refined_sentences = []

for sentence in sentences:
    refined_sentence = [beginning]
    for word in sentence:
        # Makes my life easier
        if word.isalnum():
            uppered = word.upper()
            refined_sentence.append(uppered)
    refined_sentence.append(end)
    # Skip [["<s>"], ["</s>"]] sentences
    if len(refined_sentence) > 2:
        refined_sentences.append(refined_sentence)

# Generate corpus:
stringify = [" ".join(string) for string in refined_sentences]
with open("../refined_text.txt", "w") as refined_text:
    refined_text.writelines(stringify)

total = len(stringify) # 7189
# Create a test set that is 15% of training set.
num_to_extract = math.floor(total * .15) # 1078

count = 0
test_data = []

# Grabs sequences of 11 sentences from random positions.
# The del method for whittling down the training set is inefficient,
# but this was the most intuitive way of generating a testing and training
# set that I could come up with.
while count < num_to_extract:
    random_entry_point = random.randint(0, total - 11)
    vals = stringify[random_entry_point:random_entry_point + 11]
    test_data.extend(vals)
    del stringify[random_entry_point: random_entry_point + 11]
    total = len(stringify)
    count += 11

# Write testing data
with open("../test_data.txt", "w") as test_source:
    test_source.writelines(test_data)

# Write training data
with open("../training_data.txt", "w") as training_source:
    training_source.writelines(stringify)
