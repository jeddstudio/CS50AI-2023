import nltk
import sys
import pprint


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> N V
NP -> D N | N
VP -> V | V NP

S -> NP VP

AP -> A | A AP
NP -> N | D NP | AP NP | N PP
PP -> P NP
VP -> V | V NP | V NP PP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


sentence = "holmes sat 12 a $#) A CAR"



# def main():

#     # If filename specified, read sentence from file
#     if len(sys.argv) == 2:
#         with open(sys.argv[1]) as f:
#             s = f.read()

#     # Otherwise, get sentence as input
#     else:
#         s = input("Sentence: ")

#     # Convert input into list of words
#     s = preprocess(s)

#     # Attempt to parse sentence
#     try:
#         trees = list(parser.parse(s))
#     except ValueError as e:
#         print(e)
#         return
#     if not trees:
#         print("Could not parse sentence.")
#         return

#     # Print each tree with noun phrase chunks
#     for tree in trees:
#         tree.pretty_print()

#         print("Noun Phrase Chunks")
#         for np in np_chunk(tree):
#             print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    preprocess_lst = []
    lower_sentence = sentence.lower() # convert sentence to lower case

    # Use `nltk.word_tokenize` to convert the sentence to a list
    word_lst = nltk.word_tokenize(lower_sentence) # ['holmes', 'sat', '12', 'a', '$', '#', ')', 'a', 'car']
    

    for word in word_lst:
        if word.isalpha():
            preprocess_lst.append(word)
    # ['holmes', 'sat', 'a', 'a', 'car']
    
    return preprocess_lst


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    raise NotImplementedError


# if __name__ == "__main__":
#     main()



preprocess(sentence)