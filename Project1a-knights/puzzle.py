from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")



# Puzzle 0
# A says "I am both a knight and a knave."
'''
knight always true it mans "truth"
knave always false it means "lying"
👌🏼 = Established
🙅🏻‍♂️ = Not Established
'''
knowledge0 = And(
    # TODO
    # If A=knight
        # 🙅🏻‍♂️, A NOT "lying", will NOT say "I am both a knight AND a knave"
            ###### A Not knight ######
    Implication(AKnight, Not(AKnight)),

    # If A=knave
        # 👌🏼, A is "lying"
            ###### A can be knave ######
    Implication(AKnave, AKnave),
    Or(AKnight, AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    # If A=knight
        # 🙅🏻‍♂️, A NOT "lying" (say he is knaves), 
            ###### A Not knight ######
        # what if B=knight?
        # what if B=knave? - B says nothing, he might be knight or knave
            ###### A Not knight, B can be knight or knave ######
    Implication(AKnight, And(Not(AKnight), Or(BKnight, BKnave))),

    # if A=knave
        # what if B=knight - 👌🏼, A "lying" 
            ###### B can be knight ######
        # what if B=knave - 🙅🏻‍♂️, A not telling "truth"
            ###### B Not knave ######
    Implication(AKnave, And(BKnight, Not(BKnave))),

    And(Or(AKnight, AKnave), Or(BKnight, BKnave))
)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
'''
knight always true it mans "truth"
knave always false it means "lying"
👌🏼 = Established
🙅🏻‍♂️ = Not Established
'''
knowledge2 = And(
    # TODO
    ########## A says "We are the same kind." ##########
    # If A=knight
        # what if B=knight? - 🙅🏻‍♂️, It has Contradictory: They can't both be truth 
            ###### B Not knight ######
        # what if B=knave? - 🙅🏻‍♂️, B is not "lying" 
            ###### B Not knave ######    
    Implication(AKnight, Not(Or(BKnight, BKnave))),

    # After above, A can't be knight, because if A=knight, B can't be both of be knight and knave
    Not(AKnight),

    # If A=knave
        # what if B=knight? - 👌🏼, A is "lying", B telling "truth" 
            ###### B can be knight ######
        # what if B=knave? - 🙅🏻‍♂️, A is not "lying", B is "lying"
            ###### B Not knave ######
    Implication(AKnave, And(BKnight, Not(BKnave))),

    ########## B says "We are of different kinds." ##########
    # If B=knight 
        # what if A=knight? - 🙅🏻‍♂️, B not telling "truth" 
            ###### A Not knight ######
        # what if A=knave? - 👌🏼, A is "lying", B is telling "truth",  
            ###### A can be knave ######
    Implication(BKnight, And(Not(AKnight), AKnave)),
    # A only be a knight or knave 
    Or(AKnight, AKnave),

    # If B=knave
        # what if A=knight? - 🙅🏻‍♂️, A not telling "truth" 
            ###### A Not knight ######
        # what if A=knave? - A not "lying"
            ### A Not knave ###
    Implication(BKnave, Not(Or(AKnight, AKnave))),

    # B only be a knight or knave 
    Or(AKnight, AKnave),
)



# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
'''
knight always true it mans "truth"
knave always false it means "lying"
👌🏼 = Established
🙅🏻‍♂️ = Not Established
'''
knowledge3 = And(
    # Setup the basic rule
    # A, B and C is either knight or knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),


    ########## A says either "I am a knight." or "I am a knave.", but you don't know which. ##########
    # If A=knight
        # Says "I am a knight." - 👌🏼, is telling "truth"
        # Says "I am a knave", A won't never say this if he is a knight
            ###### A is knight ######
    Implication(AKnight, AKnight),

    # If A=knave
        # Says "I am a knight." is lying
            ###### A can be knave ######
        # Says "I am a knave", 
            ### 🤔🤔 TRICKY POINT 🤔🤔 ### 
                # We are assume knave always "lying", 
                # With (A=knight never say "I am a knave") the different is knight only say "truth" (aka "I am a knight.")
                    # knave will say anything 
                        # so if "A=knave and I am a knave" come both, it will make us confuse
        # So we only can tell:
            ###### A Not Aknave ###### (instead of "A is knave") (If A=knave, it can't be a knight)
    Implication(AKnave, Not(AKnave)),


    
    ########## B says "A said 'I am a knave'." ##########
    ########## B says "C is a knave." ##########
    ##### ❗️B said two sentences, it should consider at one time#####
    ##### ❗️This follows on from A said "I am a knight." or "I am a knave." #####
    # If B=knight
        # what if A=knight - 🙅🏻‍♂️, B telling "truth",  A not telling "truth" 
            ###### A not knight ######
        # what if A=knave - 🙅🏻‍♂️, B telling "truth", this is same as the ### 🤔🤔 TRICKY POINT 🤔🤔 ### above
            ###### A Not knight ###### (use Not(Aknight) instead of "A is knave") (If A=knave, it can't be a knight)
    Implication(BKnight, Not(AKnight)),
        # what if C=knight - 🙅🏻‍♂️, knight(B) only tell "truth"
        # what if C=knave - 👌🏼, knight(B) telling "truth"
            ###### C can be knave ######
    Implication(BKnight, CKnave),
    ## It can combine like the following, but I keep above because it's easy to understand
    # Implication(BKnight, And(Not(AKnight), CKnave)),
    

    # If B=knave
        # what if A=knight - 👌🏼, B is "lying", A actually said "I am a knight"("truth") 
            ###### A can be knight ######
        # what if A=knave - 👌🏼, B is "lying", A actually said "I am a knight"("lying")
            # But We can't say that A is knave immediately
                # We need to consider what if A said "I am a knight" as he is a knight, So
            ###### A might be knave Or A might be knight ######
    Implication(BKnave, Or(AKnight, AKnave)),
    #     # what if C=knight - 👌🏼, knave(B) is "lying" that "C is a knave."
    #     # what if C=knave - 🙅🏻‍♂️, knave(B) NOT telling "truth"
    #         ###### C Not knave ######
    Implication(BKnave, Not(CKnave)),
    ## It can combine like the following, but I keep above because it's easy to understand
    # Implication(BKnave, And(Or(AKnight, AKnave), Not(CKnave))),

    ########## C says "A is a knight." ##########
    # If C=knight
        # what if A=knight? - 👌🏼, knight(C) telling "truth"
        # what if A=knave? - 🙅🏻‍♂️, knight(C) not "lying"
            ###### A can be a knight ######
    Implication(CKnight, AKnight),
    # If C=knave
        # what if A=knight? - 🙅🏻‍♂️, knave(C) telling "truth"
        # what if A=knave? - 👌🏼, knave(C) is "lying"
            ###### A can be a knave ######
    Implication(CKnave, Not(AKnight))
)





def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()