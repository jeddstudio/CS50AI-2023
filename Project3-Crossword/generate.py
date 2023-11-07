import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters


######################## Help with testing your code ########################
    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)
######################## Help with testing your code ########################





    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())



    """
    ### How the data look like ###
    structure1.txt      python generate.py data/structure1.txt data/words1.txt
    ##############      ██████████████
    #######_####_#      ███████M████R█
    #____________#      █INTELLIGENCE█
    #_#####_####_#      █N█████N████S█
    #_##_____###_#      █F██LOGIC███O█
    #_#####_####_#      █E█████M████L█
    #_###______#_#      █R███SEARCH█V█
    #######_####_#      ███████X████E█
    ##############      ██████████████ 

    # MINIMAX ➔ Variable(1, 7, 'down', 7):
    # INTELLIGENCE ➔ Variable(1, 12, 'down', 7):

    # words1.txt
    self.domain ={
        Variable(1, 7, 'down', 7): {'RECURRENT', 'CONDITION', 'BREADTH', 'DEPTH', 'BAYES', 'TRUTH', 'INFERENCE', 'TRUE', 'BYTE', 'HEURISTIC', 'BETA', 'RESOLUTION', 'LOGIC', 'CONSTRAINT', 'PROPOSITION', 'PRUNE', 'BIT', 'SINE', 'GRAPH', 'LEARNING', 'INTELLIGENCE', 'SEARCH', 'LANGUAGE', 'MARKOV', 'RESOLVE', 'ARTIFICIAL', 'LINE', 'OPTIMIZATION', 'DISTRIBUTION', 'INFER', 'NEURAL', 'PROBABILITY', 'ARC', 'UNCERTAINTY', 'INITIAL', 'CLASSIFY', 'REGRESSION', 'NETWORK', 'END', 'CLASSIFICATION', 'LOSS', 'ALPHA', 'ADVERSARIAL', 'NODE', 'CREATE', 'KNOWLEDGE', 'MINIMAX', 'START', 'SATISFACTION', 'REASON', 'FALSE'}, 
        Variable(1, 12, 'down', 7): {'RECURRENT', 'CONDITION', 'BREADTH', 'DEPTH', 'BAYES', 'TRUTH', 'INFERENCE', 'TRUE', 'BYTE', 'HEURISTIC', 'BETA', 'RESOLUTION', 'LOGIC', 'CONSTRAINT', 'PROPOSITION', 'PRUNE', 'BIT', 'SINE', 'GRAPH', 'LEARNING', 'INTELLIGENCE', 'SEARCH', 'LANGUAGE', 'MARKOV', 'RESOLVE', 'ARTIFICIAL', 'LINE', 'OPTIMIZATION', 'DISTRIBUTION', 'INFER', 'NEURAL', 'PROBABILITY', 'ARC', 'UNCERTAINTY', 'INITIAL', 'CLASSIFY', 'REGRESSION', 'NETWORK', 'END', 'CLASSIFICATION', 'LOSS', 'ALPHA', 'ADVERSARIAL', 'NODE', 'CREATE', 'KNOWLEDGE', 'MINIMAX', 'START', 'SATISFACTION', 'REASON', 'FALSE'}, 
    } 

    ### What happen here:
    # The structure1.txt is the 口 for the crossword puzzle.
    # We iterate word in the words1.txt to check if it is fit the space or not 
        # the INTELLIGENCE is fit the (1, 12) after we check this

    ###### CSP ######
    Variables is Coordinates e.g. (1, 0), (1, 7) like Sudoku
    Domains is the words
    """


######################## 🧪🧪 Testing Code in Terminal 🧪🧪 ########################
# `python generate.py data/structure1.txt data/words1.txt`

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # print(self.crossword.variables)
        # {Variable(1, 12, 'down', 7), Variable(4, 4, 'across', 5), Variable(2, 1, 'across', 12), ...}


        for var in self.crossword.variables: # `.variables` is from crossword.py ➔ `Crossword()` ➔ `def __init__()`
            print(f"This is var{var}")
            # var data like this
                # (6, 5) across : 6
                # (1, 7) down : 7
                # ...
            # Create a set() to store the values that will be removed
            to_remove_var = set()

            # Iterate all domain words 
            for word in self.domains[var]: # It will loop throught all words 1 by 1
                # `self.domains[var]` data look like {'CONDITION', 'RESOLVE', 'ARTIFICIAL', ...}
                # word look like
                    # BIT
                    # MARKOV
                    # ...

                # Check if the len(word) NOT matches the length of the var
                    # if matches, it will keep in the domains
                if len(word) != var.length: # `variables.length` is from crossword.py ➔ `class Variable()` ➔ `def __init__()` ➔ `self.length`
                    to_remove_var.add(word) # If not, add to the `to_remove_var` set()

            # Iterates to_remove_var 
            for word in to_remove_var:
                self.domains[var].remove(word) # If the word in domain, it will be Removed



    # def revise(self, x, y):
    #     """
    #     Make variable `x` arc consistent with variable `y`.
    #     To do so, remove values from `self.domains[x]` for which there is no
    #     possible corresponding value for `y` in `self.domains[y]`.

    #     Return True if a revision was made to the domain of `x`; return
    #     False if no revision was made.
    #     """
    #     raise NotImplementedError

    # def ac3(self, arcs=None):
    #     """
    #     Update `self.domains` such that each variable is arc consistent.
    #     If `arcs` is None, begin with initial list of all arcs in the problem.
    #     Otherwise, use `arcs` as the initial list of arcs to make consistent.

    #     Return True if arc consistency is enforced and no domains are empty;
    #     return False if one or more domains end up empty.
    #     """
    #     raise NotImplementedError

    # def assignment_complete(self, assignment):
    #     """
    #     Return True if `assignment` is complete (i.e., assigns a value to each
    #     crossword variable); return False otherwise.
    #     """
    #     raise NotImplementedError

    # def consistent(self, assignment):
    #     """
    #     Return True if `assignment` is consistent (i.e., words fit in crossword
    #     puzzle without conflicting characters); return False otherwise.
    #     """
    #     raise NotImplementedError

    # def order_domain_values(self, var, assignment):
    #     """
    #     Return a list of values in the domain of `var`, in order by
    #     the number of values they rule out for neighboring variables.
    #     The first value in the list, for example, should be the one
    #     that rules out the fewest values among the neighbors of `var`.
    #     """
    #     raise NotImplementedError

    # def select_unassigned_variable(self, assignment):
    #     """
    #     Return an unassigned variable not already part of `assignment`.
    #     Choose the variable with the minimum number of remaining values
    #     in its domain. If there is a tie, choose the variable with the highest
    #     degree. If there is a tie, any of the tied variables are acceptable
    #     return values.
    #     """
    #     raise NotImplementedError

    # def backtrack(self, assignment):
    #     """
    #     Using Backtracking Search, take as input a partial assignment for the
    #     crossword and return a complete assignment if possible to do so.

    #     `assignment` is a mapping from variables (keys) to words (values).

    #     If no assignment is possible, return None.
    #     """
    #     raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()