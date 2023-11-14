import math
import random
import time


class Nim():

    def __init__(self, initial=[1, 3, 5, 7]):              
        """                                                  
        Initialize game board.                                                  [1, 3, 5, 7] looks like
        Each game board has                                                             #
            - `piles`: a list of how many elements remain in each pile                 ###
            - `player`: 0 or 1 to indicate which player's turn                        #####
            - `winner`: None, 0, or 1 to indicate who the winner is                  #######
        """
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        """
        Nim.available_actions(piles) takes a `piles` list as input
        and returns all of the available actions `(i, j)` in that state.

        Action `(i, j)` represents the action of removing `j` items
        from pile `i` (where piles are 0-indexed).
        """
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        """
        Nim.other_player(player) returns the player that is not
        `player`. Assumes `player` is either 0 or 1.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = Nim.other_player(self.player)

    def move(self, action):
        """
        Make the move `action` for the current player.
        `action` must be a tuple `(i, j)`.
        """
        pile, count = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update pile
        self.piles[pile] -= count
        self.switch_player()

        # Check for a winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)



    """
    # [1, 1, 3, 5], representing the state with 1 object in pile 0, 1 object in pile 1, 3 objects in pile 2, and 5 objects in pile 3
    # `action` in the Nim game will be a pair of integers (i, j), 
        # taking j objects from pile i. 
        # `action` (3, 5) represents the action “from pile 3, take away 5 objects.” 
    # Applying that `action` to the state [1, 1, 3, 5] would result in the new state [1, 1, 3, 0] (the same state, but with pile 3 now empty).
    Return the Q-value for the state `state` and the action `action`.
    If no Q-value exists yet in `self.q`, return 0.
    """

    def get_q_value(self, state, action):
        """
        # Python dictionary can't use list as a key of dictionary
            # need to convert state from list to tuple [] ➔ () 
                # {([1, 1, 3, 5], (3, 1)): 0.9375, ...} ➔ {((1, 1, 3, 5), (3, 1)): 0.9375, ...}

        # `self.q` is a dictionary that store of trained data (e.g. 10000 times)
            # {((0, 1, 0, 1), (3, 1)): 0.9375, ((0, 1, 0, 0), (1, 1)): -0.9375}
                # q high is good, low is bad

        # `get_q_value` is using state and action (e.g. ((0, 1, 0, 1), (3, 1))) to get a `q` value
            # q_value = 0.9375
        
        # return q_value
        # return 0, if that (state, action) Not in the dictionary
        """
        # The state is [1, 3, 5, 7] when the game start
        state_tuple = tuple(state) # Convert it to (1, 3, 5, 7) for dictionary data type

        if (state_tuple, action) in self.q:
            # (state_tuple, action) ➔ (0, 1, 0, 0), (1, 1)
                # if they are in self.q
            return self.q[(state_tuple, action)] # return "-0.9375"
        else:
            return 0


    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        # Try and Calculate in the train
            # Try a (state, action)

        # Use the formula:
            # Q(s, a) <- old value estimate + alpha * (new value estimate - old value estimate)
                # `old value estimate` is the previous Q-value,
                # `alpha` is the learning rate, and 
                # `new value estimate` is the sum of the current reward and estimated future rewards.
        
        # Update a new_q for the (state, action)
        """
        # The state is [1, 3, 5, 7] when the game start
        state_tuple = tuple(state) # Convert it to (1, 3, 5, 7) for dictionary data type

        # Use the formula:
        new_q = old_q + self.alpha * ((reward + future_rewards) - old_q)
        # new value estimeate = (reward + future_rewards), the sum of "current reward + future rewards"
            # new_q: 0.9999961853027344 = 0.9999923706054688 + 0.5 * ((1 + 0) - 0.9999923706054688)


        self.q[(state_tuple, action)] = new_q
        # Assign the new_q to key:(state_tuple, action)
            # (0, 1, 0, 3) (3, 3) : 0.9980468451976771
                # It means this state and action has 0.9980468451976771


    def best_future_reward(self, state):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """
        # The state is [1, 3, 5, 7] when the game start
        state_tuple = tuple(state) # Convert it to (1, 3, 5, 7) for dictionary data type

        # A dictionary that the move can be choice
        possible_actions = Nim.available_actions(state)
            # {(1, 2), (2, 1), (3, 4), (3, 1), (3, 7), (1, 1), (3, 3), (3, 6), (3, 2), (1, 3), (3, 5)}
        
        # Initialize max Q value to 0
        max_q_value = 0

        # Check the Q-value in each `possible_action`
        for action in possible_actions:
            # action: (1, 1)

            # Use get() to get state and action, and set a defualt q_value to 0
            q_value = self.q.get((state_tuple, action), 0)
            # It will have multi state_tuple for the action
                #action: (1, 1)
                # ((0, 1, 0, 2) (1, 1): 0), ((0, 1, 0, 1) (1, 1): 0), ((0, 1, 0, 0) (1, 1): -0.984375)

            # Find the max and assign it into `max_q_value`
            if q_value > max_q_value:
                max_q_value = q_value

        # The default is 0, show if no max_q_value got, it will always return 0
        return max_q_value


    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        # A dictionary that the move can be choice
        possible_actions = Nim.available_actions(state)
            # {(1, 2), (2, 1), (3, 4), (3, 1), (3, 7), (1, 1), (3, 3), (3, 6), (3, 2), (1, 3), (3, 5)}
        
        # Initialize `best_action` adn `best_q_value`
        best_action = None
        best_q_value = float('-inf')

        # Epsilon-greedy Algorithm
            # The `epsilon` is come from `NimAI()` `def __init__`
        if epsilon: # If `epsilon` is True
            random_number = random.random() # Generate a random number
            
            if random_number < self.epsilon: 
                return random.choice(list(possible_actions))
                # use `.choice` to random pick a action(3, 6)
            
        # IF `epsilon` NOT True
            # Select the action with the highest Q in `possible_action`
        for action in possible_actions:
            q_value = self.get_q_value(state, action)
            if q_value > best_q_value:
                best_q_value = q_value
                best_action = action

        return best_action
    
    

def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    player = NimAI()

    # Play n games
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Nim()

        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Make move
            game.move(action)
            new_state = game.piles.copy()

            # When game is over, update Q values with rewards
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("Done training")

    # Return the trained AI
    return player


def play(ai, human_player=None):
    """
    Play human game against the AI.
    `human_player` can be set to 0 or 1 to specify whether
    human player moves first or second.
    """

    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = Nim()

    # Game loop
    while True:

        # Print contents of piles
        print()
        print("Piles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        print()

        # Compute available actions
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)

        # Let human make a move
        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available_actions:
                    break
                print("Invalid move, try again.")

        # Have AI make a move
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")

        # Make move
        game.move((pile, count))

        # Check for winner
        if game.winner is not None:
            print()
            print("GAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            return