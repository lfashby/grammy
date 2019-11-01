from nltk.corpus import brown
import json

sentences = brown.sents(categories="belles_lettres")

beginning = "<s>"
end = "</s>\n"
refined_sentences = []

for sentence in sentences:
    refined_sentence = [beginning]
    for word in sentence:
        if word.isalnum():
            uppered = word.upper()
            refined_sentence.append(uppered)
    refined_sentence.append(end)
    # Remove [["<s>"], ["</s>"]] sentences
    if len(refined_sentence) > 2:
        refined_sentences.append(refined_sentence)

stringify = [" ".join(string) for string in refined_sentences]

with open ("refined_text.txt", "w") as refined_text:
    refined_text.writelines(stringify)