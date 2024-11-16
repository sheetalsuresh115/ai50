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
    count_x = 0
    count_o = 0
    for row in board:
        for cell in row:
            if cell == X:
                count_x += 1
            elif cell == O:
                count_o += 1
    # If the number of X's on the board are more, then it is O's turn
    if count_x > count_o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available_actions = set()
    for index, row_element in enumerate(board):
        for col_index, col_element in enumerate(row_element):
            # Elements that are empty are available actions
            if col_element == EMPTY:
                available_actions.add((index, col_index))
    return available_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    temp_board = copy.deepcopy(board)
    next_player = player(board)

    if action[0] < 0 or action[0] >= len(board) or action[1] < 0 or action[1] >= len(board[0]):
        raise ValueError("Invalid move: move is out-of-bounds.")
    if temp_board[action[0]][action[1]] != EMPTY:
        raise ValueError("Invalid move: cell is already occupied.")

    # Player's action is added to the board
    temp_board[action[0]][action[1]] = next_player

    return temp_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check same element in columns
    if all((i is not None and i == board[0][0]) for i in board[0]):
        return board[0][0]
    elif all((i is not None and i == board[1][0]) for i in board[1]):
        return board[1][0]
    elif all((i is not None and i == board[2][0]) for i in board[2]):
        return board[2][0]
    # Check same element in columns
    elif board[0][0] == board[1][0] and board[1][0] == board[2][0]:
        return board[0][0]
    elif board[0][1] == board[1][1] and board[1][1] == board[2][1]:
        return board[0][1]
    elif board[0][2] == board[1][2] and board[1][2] == board[2][2]:
        return board[0][2]

    # Check diagonals
    elif board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    The game is over when there are no more moves available or a player has won.
    """
    # terminal board checks if a winner exists or if there are any more possible actions
    if winner(board) != None or actions(board) == set():
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Minmax algo logic is added here.
    if terminal(board):
        return None
    else:
        if player(board) == X:
            value, move = max_value(board)
            return move
        else:
            value, move = min_value(board)
            return move


def max_value(board):
    if terminal(board):
        return utility(board), None

    smallest_value = float('-inf')
    move = None
    # returns 
    for action in actions(board):
        aux, act = min_value(result(board, action))
        if aux > smallest_value:
            smallest_value = aux
            move = action
            if smallest_value == 1:
                return smallest_value, move

    return smallest_value, move


def min_value(board):
    if terminal(board):
        return utility(board), None

    largest_value = float('inf')
    move = None
    for action in actions(board):
        aux, act = max_value(result(board, action))
        if aux < largest_value:
            largest_value = aux
            move = action
            if largest_value == -1:
                return largest_value, move

    return largest_value, move
