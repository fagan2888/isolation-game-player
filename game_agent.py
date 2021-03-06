"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def my_moves(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player as number of moves the player has.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    legal_moves = game.get_legal_moves(player=player)
    return float(len(legal_moves))

def their_moves(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player as number of moves the player has.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # return negative of number of moves for the opponent
    return -float(len(game.get_legal_moves(player=game.get_opponent(player))))


def moves_diff(game, player, gamma=1.0):
    """Calculate the heuristic value of a game state from the point of view
    of the given player as number of moves the player has.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # number of moves for player
    numA = len(game.get_legal_moves(player=player))
    # number of moves for opponent
    numB = len(game.get_legal_moves(player=game.get_opponent(player)))
    return numA - gamma*numB

def blanks_diff_thiers(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player as number of moves the player has.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Number of blanks in the board
    numA = len(game.get_blank_spaces())
    # Number of moves for the opponent
    numB = len(game.get_legal_moves(player=game.get_opponent(player)))
    return float(numA - numB)

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """

    #return my_moves(game, player)
    #return moves_diff(game, player, gamma=1.5) # 72.14
    #return moves_diff(game, player, gamma=2.0) # 70.71
    #return moves_diff(game, player, gamma=0.5) # 79.29
    #return their_moves(game, player) # 72.86
    #return blanks_diff_thiers(game, player) #75.71

    # Winning evaluation function
    return moves_diff(game, player, gamma=0.5)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10., rseed=16):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        random.seed(16)

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        lastiter_move = None
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.iterative:
                # Attempt to do minimax/alphabeta for increasing depths starting with 1
                # till it hit the time limit
                depth = 1
                depthbound = len(game.get_blank_spaces())
                while depth <= depthbound:
                    #print("DEBUG>>> depth = %d" % depth, flush=True)
                    _, predmove = self.minimax(game, depth) if self.method == 'minimax' else self.alphabeta(game, depth)
                    # save the move suggested by last iteration on depth
                    lastiter_move = predmove
                    depth += 1
            else:
                # Just do minimax/alphabeta for the specified number of search_depth
                _, lastiter_move = self.minimax(game, self.search_depth) if self.method == 'minimax' else self.alphabeta(game, self.search_depth)

        except Timeout:
            # Handle any actions required at timeout, if necessary
            # if no iterations completed, then return a random move.
            if lastiter_move is None:
                lastiter_move = legal_moves[random.randint(0, len(legal_moves) - 1)]

        # Return the best move from the last completed search iteration
        return lastiter_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        ## The following implementation is based on the pseudocode for minimax algorithm
        ## given in AIMA 3ed book, Adversarial search.
        # Return the state utility if terminal
        val = game.utility(self)
        if val != 0.0:
            return val, (-1, -1)
        # Reached max depth via recursion, return the evaluation function score for CustomPlayer player.
        if depth == 0:
            return self.score(game, self), (-1, -1)
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Initialize value of current state to very high value if minimizing node and low
        # value for maximizing node
        val = -99999.0 if maximizing_player else 99999.0
        # Get all legal moves of the current active player
        legal_moves = game.get_legal_moves()
        nextmove = None
        for move in legal_moves:
            # Make a 'move' move on the boad w.r.t to current active player
            newgame = game.forecast_move(move)
            # Get the score of the new node recursively
            newscore, _ = self.minimax(newgame, depth-1, maximizing_player=(not maximizing_player))
            # If newscore is better w.r.t to 'maximizing_player', then update nextmove and val
            if (maximizing_player and (newscore > val)) or ((not maximizing_player) and (newscore < val)):
                val = newscore
                nextmove = move
        return val, nextmove

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        ## The following implementation is based on the pseudocode for
        ## alpha-beta pruning algorithm given in AIMA 3ed book, Adversarial search.
        # Return the state utility if terminal
        val = game.utility(self)
        if val != 0.0:
            return val, (-1, -1)
        # Reached max depth via recursion, return the evaluation function score for CustomPlayer player.
        if depth == 0:
            return self.score(game, self), (-1, -1)
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Initialize value of current state to very high value if minimizing node and low
        # value for maximizing node
        val = -99999.0 if maximizing_player else 99999.0
        # Get all legal moves of the current active player
        legal_moves = game.get_legal_moves()
        # shuffle the moves list to try avoid any unlucky sets of orderings that allow less pruning
        random.shuffle(legal_moves)
        nextmove = None
        for move in legal_moves:
            # Make a 'move' move on the boad w.r.t to current active player
            newgame = game.forecast_move(move)
            # Get the score of the new node recursively
            newscore, _ = self.alphabeta(newgame, depth-1, alpha=alpha, beta=beta, maximizing_player=(not maximizing_player))
            # If newscore is better w.r.t to 'maximizing_player', then update nextmove and val
            if (maximizing_player and (newscore > val)) or ((not maximizing_player) and (newscore < val)):
                val = newscore
                nextmove = move
            # For a given min/max node, if val is poorer than its bound, then no need to evaluate its other siblings.
            if (maximizing_player and val >= beta) or ((not maximizing_player) and val <= alpha):
                return val, nextmove
            if maximizing_player:
                alpha = max(alpha, val)
            else:
                beta = min(beta, val)
        return val, nextmove

