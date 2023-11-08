# test.py
from generate import CrosswordCreator
from crossword import Crossword

# 指定結構檔和單詞檔的路徑
STRUCTURE_FILE = 'data/structure1.txt'
WORDS_FILE = 'data/words1.txt'

def main():
    # 創建一個 Crossword 實例
    crossword = Crossword(STRUCTURE_FILE, WORDS_FILE)
    creator = CrosswordCreator(crossword)

    print("原始變量域:")
    for variable in creator.crossword.variables:
        print(variable, creator.domains[variable])

    # 呼叫 enforce_node_consistency 並顯示結果
    creator.enforce_node_consistency()
    print("\n應用 enforce_node_consistency 後的變量域:")
    for variable in creator.crossword.variables:
        print(variable, creator.domains[variable])
    












if __name__ == "__main__":
    main()


##############      ██████████████
#######_####_#      ███████M████R█
#____________#      █INTELLIGENCE█
#_#####_####_#      █N█████N████S█
#_##_____###_#      █F██LOGIC███O█
#_#####_####_#      █E█████M████L█
#_###______#_#      █R███SEARCH█V█
#######_####_#      ███████X████E█
##############      ██████████████ 

# MINIMAX ➡️ Variable(1, 7, 'down', 7):
# INTELLIGENCE ➡️ Variable(1, 12, 'down', 7):
# { 
#     Variable(1, 7, 'down', 7): {'RECURRENT', 'CONDITION', 'BREADTH', 'DEPTH', 'BAYES', 'TRUTH', 'INFERENCE', 'TRUE', 'BYTE', 'HEURISTIC', 'BETA', 'RESOLUTION', 'LOGIC', 'CONSTRAINT', 'PROPOSITION', 'PRUNE', 'BIT', 'SINE', 'GRAPH', 'LEARNING', 'INTELLIGENCE', 'SEARCH', 'LANGUAGE', 'MARKOV', 'RESOLVE', 'ARTIFICIAL', 'LINE', 'OPTIMIZATION', 'DISTRIBUTION', 'INFER', 'NEURAL', 'PROBABILITY', 'ARC', 'UNCERTAINTY', 'INITIAL', 'CLASSIFY', 'REGRESSION', 'NETWORK', 'END', 'CLASSIFICATION', 'LOSS', 'ALPHA', 'ADVERSARIAL', 'NODE', 'CREATE', 'KNOWLEDGE', 'MINIMAX', 'START', 'SATISFACTION', 'REASON', 'FALSE'}, 
#     Variable(1, 12, 'down', 7): {'RECURRENT', 'CONDITION', 'BREADTH', 'DEPTH', 'BAYES', 'TRUTH', 'INFERENCE', 'TRUE', 'BYTE', 'HEURISTIC', 'BETA', 'RESOLUTION', 'LOGIC', 'CONSTRAINT', 'PROPOSITION', 'PRUNE', 'BIT', 'SINE', 'GRAPH', 'LEARNING', 'INTELLIGENCE', 'SEARCH', 'LANGUAGE', 'MARKOV', 'RESOLVE', 'ARTIFICIAL', 'LINE', 'OPTIMIZATION', 'DISTRIBUTION', 'INFER', 'NEURAL', 'PROBABILITY', 'ARC', 'UNCERTAINTY', 'INITIAL', 'CLASSIFY', 'REGRESSION', 'NETWORK', 'END', 'CLASSIFICATION', 'LOSS', 'ALPHA', 'ADVERSARIAL', 'NODE', 'CREATE', 'KNOWLEDGE', 'MINIMAX', 'START', 'SATISFACTION', 'REASON', 'FALSE'}, 
# }   



