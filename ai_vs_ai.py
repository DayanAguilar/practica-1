import time
import random
import copy
from utils import (
    BLACK,
    WHITE,
    EMPTY,
    forms_square,
    forms_corners,
    make_move,
    get_opponent,
    traduction_move,
)
SPACE = "---|---|---|---"

def terminal_test(board, player):

    for i in range(4):
        if board[i] == [player, player, player, player]:
            return True

    for j in range(4):
        if [board[x][j] for x in range(4)] == [player, player, player, player]:
            return True

    if (
        board[0][0] == player
        and board[0][3] == player
        and board[3][0] == player
        and board[3][3] == player
    ):
        return True

    for i in range(3):
        for j in range(3):
            if (
                board[i][j] == player
                and board[i][j + 1] == player
                and board[i + 1][j] == player
                and board[i + 1][j + 1] == player
            ):
                return True

    return False

def count_adjacent_pieces(board, row, col, player):
    adjacent_directions = [
        (1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)
    ]
    count = 0
    for dr, dc in adjacent_directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
            if board[new_row][new_col] == player:
                count += 1
    return count

def find_adjacencies(board):
    number_b_adj = 0
    number_w_adj = 0

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == BLACK:
                number_b_adj += count_adjacent_pieces(board, i, j, BLACK)
            elif board[i][j] == WHITE:
                number_w_adj += count_adjacent_pieces(board, i, j, WHITE)

    return number_b_adj, number_w_adj

def second_evaluation_function(state):
    board = state[0]
    weights = [[3, 2, 2, 3], [2, 1, 1, 2], [2, 1, 1, 2], [3, 2, 2, 3]]

    player1_score = 0
    player2_score = 0

    for i in range(4):
        for j in range(4):
            if board[i][j] == BLACK:
                player1_score += weights[i][j]
            elif board[i][j] == WHITE:
                player2_score += weights[i][j]

    adj1, adj2 = find_adjacencies(board)
    value = (player1_score - adj1) - (player2_score - adj2)
    return value


def is_winning_or_creates_special_case(temp_board, player):
    return (
        terminal_test(temp_board, player) > 0
        or forms_square(temp_board, player)
        or forms_corners(temp_board, player)
    )

def get_all_moves(board, player):
    """
    Returns all available moves for a given player on the current board.
    """
    moves = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == EMPTY:
                # Simulate the move
                temp_board = copy.deepcopy(board)
                temp_board[i][j] = player

                # Check if the move results in a win or special conditions
                if is_winning_or_creates_special_case(temp_board, player):
                    moves.append((i, j))
                    continue

                # Otherwise, add the move to the list of available moves
                moves.append((i, j))

    return moves


def first_evaluation_function(state):
    board = state[0]

    weights = [[2, 2, 2, 2], [2, 1, 1, 2], [2, 1, 1, 2], [2, 2, 2, 2]]

    player1_score = 0
    player2_score = 0

    for i in range(4):
        for j in range(4):
            if board[i][j] == BLACK:
                player1_score += weights[i][j]
            elif board[i][j] == WHITE:
                player2_score += weights[i][j]

    player1_moves = len(get_all_moves(board, BLACK))
    player2_moves = len(get_all_moves(board, WHITE))

    value = player1_score - player2_score + (player1_moves - player2_moves) * 0.1
    return value


def alpha_beta_prunning_depth_1(
    state, depth, alpha, beta, maximizing_player, available_moves, counter
):
    board, player = state
    counter += 1

    if depth == 0 or terminal_test(board, BLACK) > 0 or terminal_test(board, WHITE) > 0:
        return first_evaluation_function(state), None, counter

    best_move = None
    best_value = float("-inf") if maximizing_player else float("inf")
    
    for move in available_moves:
        new_board = make_move(board, move, player)
        new_state = [new_board, get_opponent(player)]
        
        value, _, counter = alpha_beta_prunning_depth_1(
            new_state, depth - 1, alpha, beta, not maximizing_player, available_moves, counter
        )

        if maximizing_player:
            if value > best_value:
                best_value, best_move = value, move
            alpha = max(alpha, best_value)
        else:
            if value < best_value:
                best_value, best_move = value, move
            beta = min(beta, best_value)

        if beta <= alpha:
            break

    return best_value, best_move, counter

def alpha_beta_prunning_depth_2(
    state, depth, alpha, beta, maximizing_player, available_moves, counter
):
    board, player = state
    counter += 1

    if depth == 0 or terminal_test(board, BLACK) > 0 or terminal_test(board, WHITE) > 0:
        return second_evaluation_function(state), None, counter

    best_move = None
    best_value = float("-inf") if maximizing_player else float("inf")
    
    for move in available_moves:
        new_board = make_move(board, move, player)
        new_state = [new_board, get_opponent(player)]

        value, _, counter = alpha_beta_prunning_depth_2(
            new_state, depth - 1, alpha, beta, not maximizing_player, available_moves, counter
        )

        if maximizing_player:
            if value > best_value:
                best_value, best_move = value, move
            alpha = max(alpha, best_value)
        else:
            if value < best_value:
                best_value, best_move = value, move
            beta = min(beta, best_value)

        if beta <= alpha:
            break

    return best_value, best_move, counter


def create_board():
    board = [[None for _ in range(4)] for _ in range(4)]
    board[0][0] = "B"
    board[0][3] = "W"
    board[1][1] = "B"
    board[1][2] = "W"
    board[2][1] = "W"
    board[2][2] = "B"
    board[3][0] = "W"
    board[3][3] = "B"
    return board

# Define the function for checking if a player has won

def check_win(board, player):

    for i in range(4):
        if board[i] == [player, player, player, player]:
            return True

    for j in range(4):
        if [board[x][j] for x in range(4)] == [player, player, player, player]:
            return True

    if (
        board[0][0] == player
        and board[0][3] == player
        and board[3][0] == player
        and board[3][3] == player
    ):
        return True

    for i in range(3):
        for j in range(3):
            if (
                board[i][j] == player
                and board[i][j + 1] == player
                and board[i + 1][j] == player
                and board[i + 1][j + 1] == player
            ):
                return True

    return False

# Define the function for displaying the game board

def display_board(board):
    columns = "   A   B   C   D"
    print(columns)
    for i, row in enumerate(board):
        row_display = " | ".join([cell or " " for cell in row])
        print(f"{i+1}  {row_display}")
        if i < len(board) - 1:
            print(SPACE)

def get_direction_offset(direction):
    direction_map = {
        "N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1),
        "NW": (-1, -1), "NE": (-1, 1), "SW": (1, -1), "SE": (1, 1)
    }
    return direction_map.get(direction, (0, 0))

def is_out_of_bounds(row, col, board):
    return row < 0 or col < 0 or row >= len(board) or col >= len(board[0])

def is_occupied(row, col, board, player):
    cell = board[row][col]
    return cell == player or cell == get_opponent(player)

def is_possible_move(direction, row, col, board, player):
    row_offset, col_offset = get_direction_offset(direction)
    new_row, new_col = row + row_offset, col + col_offset

    if is_out_of_bounds(new_row, new_col, board):
        return False

    if is_occupied(new_row, new_col, board, player):
        return False

    return True


def get_computer_move1(state):
    board = state[0]
    player = state[1]
    available_moves = get_available_moves(board, player)
    if not available_moves:
        return None
    max_depth = 3
    counter = 0
    _, best_move, counter = alpha_beta_prunning_depth_1(
        state, max_depth, float("-inf"), float("inf"), True, available_moves, counter
    )
    print("Number of states expanded: ", counter)
    return best_move


def get_available_moves(board, player):
    available_moves = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == player:
                available_moves.extend(generate_moves(i, j, board, player))
    return available_moves
def generate_moves(i, j, board, player):
    directions = ["N", "S", "E", "W", "NW", "NE", "SW", "SE"]
    moves = []
    for direction in directions:
        move = f"{chr(ord('A') + j)}{i + 1} {direction}"
        row, col, direction = traduction_move(move)
        if is_possible_move(direction, row, col, board, player):
            moves.append(move)
    return moves


def get_computer_move2(state):
    board, player = state
    available_moves = get_available_moves(board, player)
    if not available_moves:
        return None
    max_depth = 3
    counter = 0
    _, best_move, counter = alpha_beta_prunning_depth_2(
        state, max_depth, float("-inf"), float("inf"), True, available_moves, counter
    )
    print("Number of states expanded: ", counter)
    return best_move

def get_available_moves(board, player):
    available_moves = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == player:
                available_moves.extend(generate_moves(i, j, board, player))
    return available_moves

def generate_moves(i, j, board, player):
    directions = ["N", "S", "E", "W", "NW", "NE", "SW", "SE"]
    moves = []
    for direction in directions:
        move = f"{chr(ord('A') + j)}{i + 1} {direction}"
        row, col, direction = traduction_move(move)
        if is_possible_move(direction, row, col, board, player):
            moves.append(move)
    return moves

# Define the function for playing the game

def play_game():
    board = create_board()
    display_board(board)

    a1 = random.choice([BLACK, WHITE])


    player = BLACK  # set player to always be black
    state = (board, player)
    move = None
    while not check_win(board, BLACK) and not check_win(board, WHITE):
        if player == a1:
            move = get_computer_move1(state)
            print("Computer's move: ", move)
            board = make_move(board, move, player)

            state = (board, get_opponent(player))
            display_board(board)

        else:
            move = get_computer_move2(state)
            print("Computer's move: ", move)

        try:
            board = make_move(board, move, player)

            state = (board, get_opponent(player))
            display_board(board)
        except ValueError as e:
            print(e)

        player = get_opponent(player)

    print("Game over! Winner: ", get_opponent(player))


play_game()
