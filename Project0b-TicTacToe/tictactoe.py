"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]



def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_num = 0
    o_num = 0
    for board_state in board:
        for xo in board_state:
            if xo == X:
                x_num += 1
            elif xo == O:
                o_num += 1

    if x_num <= o_num: # If x_num=0, The game has not started yet
        return X
    else:
        return O



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Contain all possible actions
    action_set = set()

    # Get the total board size
    # TicTacToe is 9, Chessboard is 64
    board_size = len(board)
    
    # Help to understanding
    # board[0] = ["A", "B", "C"]
    # board[1] = ["D", "E", "F"]
    # board[2] = ["G", "H", "I"]

    # (i, j), it means x, y axis, I prefer use (x, y)
    for x in range(board_size):
        for y in range(board_size):
            # board x0,y0="A" ➔ board x0,y1="B" ➔ board x0,y2="C"
            # "F"= 1 2, "G" = 2 0
            if  board[x][y] == None:
                action_set.add((x, y))

    return action_set



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_move = action # a tuple like (2, 1)
    if player_move not in actions(board):
        raise ValueError(f"You can't make this move.")
    
    row, column = player_move

    # Create a deep copy of currently board state
    new_board_state = copy.deepcopy(board)
    new_board_state[row][column] = player(board) # add "X" or "O"

    return new_board_state




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check horizontally for "X" and "O" wins
    # Check as a whole row each time like this (X, O, X)
    for row in board:
        # Initialise to ensure that elements are correct to start on every loop.
        x_row = True # Assume all elements in the row are "X"
        o_row = True # Assume all elements in the row are "O"

        for xo in row:
            if xo != X: # if (X, O, X) = False, if (X, X, X) = True
                x_row = False
            if xo != O:
                o_row = False

        if x_row: # if x_row = True
            return X # Exit the loop if "X" wins vertically

        if o_row:
            return O
        # Exit the loop early if a win has been found


    # Check vertically for "X" and "O" wins
    # `range(len(board[0]))` Use the length of the first row to determine how many columns there are.
    for column in range(len(board[0])): 
        x_column = True  # Assume all elements in the column are "X"
        o_column = True  # Assume all elements in the column are "O"

        for row in range(len(board)): # In TicTacToe this is 3 ([[A,X,O],[B,X,X],[C,O,X]])
            cell = board[row][column] # It will be (0,0) ➔ (1,0) ➔ (2,0) which the order is A B C

            # Differet from the horizontally
            # Here is check 1 by 1 
            if cell != X: # If one of the values in the column is not "X"
                x_column = False  # not "X" wins
            
            if cell != O: # If one of the values in the column is not "O"
                o_column = False  # not "O" wins

        if x_column: # if x_column = True
            return X  # Exit the loop if "X" wins vertically

        if o_column:
            return O 
        # Exit the loop early if a win has been found


    # Check dagonally for "X" and "O" wins
    # Only 2 type of  dagonally "left to right" and "right to left"      
    dagonally_1 = board[0][0], board[1][1], board[2][2] # "left to right"
    dagonally_2 = board[0][2], board[1][1], board[2][0] # "right to left"
    x_end = ("X", "X", "X")
    o_end = ("O", "O", "O")

    if dagonally_1 == x_end or dagonally_2 ==  x_end:
        return X
    if dagonally_1 == o_end or dagonally_2 == o_end:
        return O
    # If no winner
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if actions() is empty the game is over, player can't take a move
    if not actions(board): 
        return True
    # if winner() return X or O, there has a winner, Game Over
    elif winner(board) != None:
        return True # Game Over
    else:
        return False # Game is still in progress



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0
    raise Exception("Error of Utility")



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board): # If the game is over, return None
        return None

    # Max Player Function
    def max_value(board):
        if terminal(board): # When the game end
            return utility(board), None # None is meaning no action to return
            
        v = float('-inf') # the lecture provided `v = -∞`
        best_action = None # Container for the player action that we will return
        
        # Walk through all possible actions 
        # Let say actions() return {(0, 1), (0, 2), (1, 2)}, we put them into loop 1 by 1
        for action in actions(board): 
            
            # Use `min_value(result())` to simulat each step of the opponent and get a score `v`
            min_v, _ = min_value(result(board, action))
            # min_value(result()) will give us a tuple like (-1, (0, 2)) or (0, None) or (0, (1, 2))
            # We don't the part (0, 2), so use `_` to ignore it
                # min_v = -1, nothing to put in `_` it just be ignored
            # the min_v is the v, in TicTacToe it would be -1, 0, 1
            # in Max player, it don't want -1


            # That's why we need  `v = -∞` at the start, 
                # we don't know what is min_v at the start(although we know that is -1 in TicTacToe)
            if min_v > v: # if 0 > -1(When find a value > the starting v)
                # Algorithm will these 2 variable during the process
                v = min_v
                best_action = action
        # When all possible actions has been walk through  
        return v, best_action


    # Min Player Function
    # It's basically the same as Max player
    def min_value(board):
        if terminal(board):
            return utility(board), None
            
        v = float('inf')
        best_action = None
        
        for action in actions(board):
            max_v, _ = max_value(result(board, action))
            # in Min player, it don't want 1
            if max_v < v: # if 0 < 1(When find a value < the starting v)
                v = max_v
                best_action = action

        return v, best_action


    # Based on X or O turn, call max_value or min_value
    if player(board) == X:
        _, best_move = max_value(board)
        # It will retrun `1 (0, 1)`
            # 1 is v and (0, 1) is the action
            # We don't the `v`, so use `_` to ignore it
    else:
        _, best_move = min_value(board)

    return best_move
