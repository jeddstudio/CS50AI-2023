import nltk
import sys

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

# CP = Complete Phrase, POS = parts of speech 8 7
NONTERMINALS = """
S -> NP VP | CP Conj CP
CP -> NP VP | VP

NP -> N | N PP | POS NP | POS P NP | NP POS NP

VP -> V | V NP | V NA | V PP | POS VP

POS -> Adj | Adv | Det 

PP -> P | P NP | POS
"""


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


# ############ Using the 3.txt for demo We arrived the day before Thursday. ############

# ############ This is `trees` ############
# [Tree('S', [Tree('NP', [Tree('N', ['we'])]), Tree('VP', [Tree('V', ['arrived']), Tree('NP', [Tree('Det', ['the']), Tree('N', ['day'])]), 
# Tree('PP', [Tree('P', ['before']), Tree('NP', [Tree('N', ['thursday'])])])])]), Tree('S', [Tree('NP', [Tree('N', ['we'])]), Tree('VP', 
# [Tree('V', ['arrived']), Tree('NP', [Tree('Det', ['the']), Tree('NP', [Tree('N', ['day'])])]), Tree('PP', [Tree('P', ['before']), 
# Tree('NP', [Tree('N', ['thursday'])])])])]), Tree('S', [Tree('NP', [Tree('N', ['we'])]), Tree('VP', [Tree('V', ['arrived']), 
# Tree('NP', [Tree('Det', ['the']), Tree('NP', [Tree('N', ['day']), Tree('PP', [Tree('P', ['before']), Tree('NP', [Tree('N', ['thursday'])])])])])])])]


# ###### This is how `tree` look like######
# (S
#   (NP (N we))
#   (VP
#     (V arrived)
#     (NP (Det the) (NP (N day) (PP (P before) (NP (N thursday)))))))
# ########################


# ############ `tree.pretty_print()` ############
#              S                             
#   ___________|___                           
#  |               VP                        
#  |      _________|___                       
#  |     |             NP                    
#  |     |      _______|____                  
#  |     |     |            NP               
#  |     |     |    ________|_____            
#  |     |     |   |              PP         
#  |     |     |   |         _____|_____      
#  NP    |     |   |        |           NP   
#  |     |     |   |        |           |     
#  N     V    Det  N        P           N    
#  |     |     |   |        |           |     
#  we arrived the day     before     thursday
# ############ `tree.pretty_print()` ############


def preprocess(sentence):
    """
    - Pre-process sentence by converting all characters to lowercase
    - Convert `sentence` to a list of its words.
    - removing any word that does not contain at least one alphabetic character.
    """
    #  sentence = We arrived the day before Thursday.

    preprocess_list = []
    lower_sentence = sentence.lower() # convert sentence to lower case

    # Use `nltk.word_tokenize` to convert the sentence to a list
    word_list = nltk.word_tokenize(lower_sentence) 
    # ['we', 'arrived', 'the', 'day', 'before', 'thursday', '.']

    for word in word_list:
        if word.isalpha(): # only alphabetic character
            preprocess_list.append(word)
    
    # preprocess_list = ['we', 'arrived', 'the', 'day', 'before', 'thursday']
    return preprocess_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    
    Returns:
    list: A list of nltk.Tree objects, each representing a noun phrase chunk
    """
    #  sentence = We arrived the day before Thursday.
    # ###### This is how `tree` look like######
    # (S
    #   (NP (N we))
    #   (VP
    #     (V arrived)
    #     (NP (Det the) (NP (N day) (PP (P before) (NP (N thursday)))))))
    # ########################
    chunks_list = []

    for subtree in tree.subtrees():
        # `subtree` will loop throught S, (NP (N we)), NP, ...

        if subtree.label() == 'NP': # If `subtree` has "NP", e.g. "(NP (N we))"

            if not any(child.label() == 'NP' for child in subtree): 
            # Check if there are any "NP" in the current "NP"
                # If not, add this "NP" into `chunks_list`
                chunks_list.append(subtree)
                # (NP (N we))
                # (NP (N day) (PP (P before) (NP (N thursday)))) 
                # (NP (N thursday))

    return chunks_list
    # chunks_list = [Tree('NP', [Tree('N', ['we'])]), Tree('NP', [Tree('N', ['day']), 
    #               Tree('PP', [Tree('P', ['before']), Tree('NP', [Tree('N', ['thursday'])])])]), 
    #               Tree('NP', [Tree('N', ['thursday'])])]
    


if __name__ == "__main__":
    main()
