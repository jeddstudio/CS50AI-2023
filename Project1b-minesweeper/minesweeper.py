import itertools
import random
import copy

HEIGHT = 8
WIDTH = 8


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        # Here received inform like the following
        # Cells: {(5, 5), (3, 4), (4, 3), (5, 4), (4, 5), (3, 3), (5, 3), (3, 5)}
        # count: 1
            # The "count" is that number it displays when you reveal a cell
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # When len(cells) == count
            # these cells must be mines.
        if len(self.cells) == self.count:
            # len((5, 5), (3, 4)) == count:2, 
                # so it 2 cells is mines
            return self.cells # return cells that are confirmed to be mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # When count == 0
            # it means no mine in it
        if self.count == 0: 
            return self.cells # return cells that are confirmed to be safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # If this def is called, it will take a cell e.g.(4, 5)
        if cell in self.cells: # Check if the cell(4, 5) is in the cells
            self.cells.remove(cell) # Remove it, cus it's been handled.
            self.count -= 1 # Update the count
        else:
            pass

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # If this def is called, it will take a cell e.g.(4, 5)
        if cell in self.cells: # Check if the cell is in the cells
            self.cells.remove(cell) # Remove it, cus it's been handled.
        else:
            pass


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []
            # something like {(6, 6), (5, 4), (5, 5), (5, 6)} = 3 


    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell) # Add the cell to `self.mines`
        for sentence in self.knowledge:
            sentence.mark_mine(cell) # Here is calling Sentence()'s `mark_mine`


    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell) # Add the cell to `self.safes`
        for sentence in self.knowledge:
            sentence.mark_safe(cell) # Here is calling Sentence()'s `mark_safe`


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
 
        # 1) mark the cell as a move that has been made
            # Let the computer know that this cell has been explored
        self.moves_made.add(cell)


        # 2) mark the cell as safe
            # And this cell not make the game over
        self.mark_safe(cell)


        # 3) add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        unknown_cells = set()
        count_deepcopy = copy.deepcopy(count) # Working on the copy and No change to the original count


        # It will generate cells that around the input cell
        neighbour_cells = self.neighbour_cells(cell) 
        # if the cell is (5, 3)
            # It return {(2, 4), (1, 2), (0, 4), (0, 3), (1, 4), (2, 3), (0, 2), (2, 2)}


        # iterates neighbour checking for mines and safes or not
        for check_cell in neighbour_cells:
            if check_cell in self.mines:
                count_deepcopy -= 1 # if it has mine, need to edit the count

            # if not mine or safe, add it to the unknown_cells
            if check_cell not in self.mines and check_cell not in self.safes:
                unknown_cells.add(check_cell)

        # Generate new sentence and put the `unknown_cells`, `count_deepcopy` into it
        new_sentence = Sentence(unknown_cells, count_deepcopy)

        # If new_sentence not empty we can add it into the `self.knowlegde`
        if len(new_sentence.cells) > 0: 
            self.knowledge.append(new_sentence)


        ############### Dealing with `self.knowledge` ###############
        # Check and mark the cell if it is empty, safe or mine
        self.knowledge_checking() 

        # AI Part here
        self.ai_inference()


        # # Check the knowledge if needed in development phase
        # for sentence in self.knowledge:
        #     print("Knowledge")
        #     print(sentence)



    def neighbour_cells(self, cell):    
        ############### Generate all cell's neighbour (x, y) ###############
        # If the cell is (3,3), We want to add all the cells around it 
        # "(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)"
        neighbours = set()

        # Using the loop to do the math to get neighbour around the cell(3,3)
        # [(2,2), (2,3), (2,4)]                                 # [(-1,-1), (0,0), (1,1)]
        # [(3,2), (3,3), (3,4)]                                 # [(-1,-1), (0,0), (1,1)]
        # [(4,2), (4,3), (4,4)]                                 # [(-1,-1), (0,0), (1,1)]
                                                                # ------------ If the cell is (3,3) ------------  # ############ The cell itself(3,3) ############
        for neighbour_x in [-1, 0, 1]:                          # x = -1, y = -1                                  # x = 0, y = 0
            for neighbour_y in [-1, 0, 1]:                      # cell[0][1] = (3, 3)                             # cell[0][1] = (3, 3)
                neighbour_row = cell[0] + neighbour_x           # cell[0]: 3 + x: -1 = row: 2                     # cell[0]: 3 + x: 0 = row: 3
                neighbour_col = cell[1] + neighbour_y           # cell[1]: 3 + y: -1 = col: 2                     # cell[1]: 3 + y: 0 = col: 3
                                                                # neighbour_row = 2, neighbour_col = 2            # neighbour_row = 3, neighbour_col = 3
                if (0 <= neighbour_row < HEIGHT and             # 0 <= 2 < HEIGHT                                 # 0 <= 3 < HEIGHT
                    0 <= neighbour_col < WIDTH and              # 0 <= 2 < WIDTH                                  # 0 <= 3 < WIDTH 
                    (neighbour_x, neighbour_y)!= (0, 0)):       # (-1, -1)!= (0, 0)) # false                      # (0, 0)!= (0, 0)) # true
                    # skips the iteration the cell itself(3,3)  # it means not the cell itself                    # it means the cell itself
                                                                # ----------------------------------------------  # #############################################

                    # Check if the cell(e.g. (2,2)) is in `mark_safe` or `mark_mine` 
                        # if not, add to `neighbours`
                    neighbours.add((neighbour_row, neighbour_col))

        return neighbours


                        
    def knowledge_checking(self):
        # Working on the copy and No change to the original knowledge
        knowledge_deepcopy = copy.deepcopy(self.knowledge) 

        for sentence in knowledge_deepcopy:

            ###### Remove all empty sentence ######
            ### A ValueError must occur everytime and must be handled ###
            if len(sentence.cells) == 0:
                try:
                    self.knowledge.remove(sentence)
                except ValueError:
                    pass
            
            ###### All neighbours is mine ######
            ### Calling the Sentence()'s `know_mines()`
            is_mines = sentence.known_mines()
            # If it no empty
            if is_mines:                         
                for cell in is_mines:           # Iterates all cell in is_mines      
                    self.mark_mine(cell)        # Add the mine cell into the MinesweeperAI()'s `mark_mine` aka let the AI knows where is the mine
                    self.knowledge_checking()   # Recursive: call itself so it can make sure all cells are processed
                # If is_mines == False, it will stop the recursive
            
            ###### No neighbours is mine ######
            ### Calling the Sentence()'s `know_safes()`
            is_safes = sentence.known_safes()
            if is_safes:                    
                for cell in is_safes:            # Iterates all cell in is_safe 
                    self.mark_safe(cell)        # Add the mine cell into the MinesweeperAI()'s `mark_safe` aka let the AI knows where is the safe
                    self.knowledge_checking()   # Recursive: call itself so it can make sure all cells are processed
                # If is_safe == False, it will stop the recursive



    # 5) add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
    def ai_inference(self):      
                     
        for sen_A in range(len(self.knowledge)):                # Assume this is 3 sentences here   
            sentence_1 = self.knowledge[sen_A]                  # sentence1 = [(2,2), (2,3), (2,4)]                             
            for sen_B in range(sen_A+1, len(self.knowledge)):   # sentence2 = [(4,2), (4,3), (4,4)]
                sentence_2 = self.knowledge[sen_B]              
                # Then we need to compare sentences 1 by 1 like the following
                    # "Comparing Sentence 1 ([(2, 2), (2, 3), (2, 4)]) with Sentence 3 ([(4,2), (4,3), (4,4)])"

                ###### Initialize new_sentence to None ######
                new_sentence = None
                #############################################

                ###### Compare sentences ######
                ### Use the Python build-in funciton `.issubset()` ###
                    # to check whether one set is a subset of another set
                    # Assume we have a knowledge_base
                        #   Sentence({(2,2), (2,3)}, 1),                 # Sentence 1
                        #   Sentence({(2,2), (2,3), (2,4)}, 2),         # Sentence 2
                        #   Sentence({(4,2), (4,3), (4,4)}, 1),         # Sentence 3
                if sentence_1.cells.issubset(sentence_2.cells):
                # (sentence_1.({(2,2), (2,3)}, 1).issubset(sentence_2.({(2,2), (2,3), (2,4)}, 2)
                    new_cells = set(sentence_2.cells) - set(sentence_1.cells)   # new_cells:{(2, 4)}
                    new_count = sentence_2.count - sentence_1.count             # new_count:1 (2-1)
                    new_sentence = Sentence(new_cells, new_count)               # new_sentence: Cells: {(2, 4)}, Count: 1
                    
                    # Check for new sentence cell are there any mines or safes
                        # If yes, add to the MinesweeperAI()'s `mark_mine` or `mark_safe`
                    is_mines = new_sentence.known_mines()
                    is_safes = new_sentence.known_safes()
                    if is_mines:
                        for mine in is_mines:
                            self.mark_mine(mine)
                    if is_safes:
                        for safe in is_safes:
                            self.mark_safe(safe)

                # Interactive Check
                if sentence_2.cells.issubset(sentence_1.cells):
                    new_cells = set(sentence_1.cells) - set(sentence_2.cells)  # same as above that how it works
                    new_count = sentence_1.count - sentence_2.count
                    new_sentence = Sentence(new_cells, new_count)             
                    is_mines = new_sentence.known_mines()
                    is_safes = new_sentence.known_safes()
                    if is_mines:
                        for mine in is_mines:
                            self.mark_mine(mine)
                    if is_safes:
                        for safe in is_safes:
                            self.mark_safe(safe)



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Use the MinesweeperAI()'s known safes to take a move
        for move in self.safes:
            if move not in self.moves_made:
                return move
        return None # No Safe move can take

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper 
        """
        # If no known safes, this def will be called
        row = random.randint(0, HEIGHT-1)
        column = random.randint(0, WIDTH-1)

        random_move = (row, column)

        if random_move not in self.mines and random_move not in self.moves_made:
            return random_move
        else:
            return None