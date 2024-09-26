import time
import random
import sys
from utils import make_move, BLACK, WHITE, get_opponent



def find_adjacencies(board):
    adjecencies = {BLACK:0, WHITE:0}
    values = {BLACK:1, WHITE:-1}
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for i in range(3):
        for j in range(3):
                for offset_i, offset_j in offsets:
                    color = board[i + offset_i][j + offset_j]
                    if 0 <= i + offset_i < 3 and 0 <= j + offset_j < 3 and color != " " and color != None: 
                        adjecencies[color] += values[color]

    return adjecencies[BLACK], adjecencies[WHITE]


def terminal_test(board, player):
    for i in range(4):
        if board[i] == [player, player, player, player]:
            return True

    for j in range(4):
        if [board[x][j] for x in range(4)] == [player, player, player, player]:
            return True

    if board[0][0] == player and board[0][3] == player and board[3][0] == player and board[3][3] == player:
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == player and board[i][j+1] == player and board[i+1][j] == player and board[i+1][j+1] == player:
                return True

    return False


def utility(state):
    opponent = get_opponent(state[1])
    if terminal_test(state[0], state[1]):
        return 100
    elif terminal_test(state[1], opponent):
        return -100
    else:
        return 0


def alpha_beta_pruning(state, alpha, beta, maximizing_player, available_moves):
    board, player = state
    if terminal_test(board, BLACK) or terminal_test(board, WHITE):
        return utility(state), None
    
    if maximizing_player:
        return maximize_value(board, player, alpha, beta, available_moves)
    else:
        return minimize_value(board, player, alpha, beta, available_moves)

def maximize_value(board, player, alpha, beta, available_moves):
    max_value = float('-inf')
    best_move = None

    for move in available_moves:
        new_value, _ = evaluate_move(board, player, move, alpha, beta, False, available_moves)
        if new_value > max_value:
            max_value, best_move = new_value, move
        alpha = max(alpha, max_value)
        if beta <= alpha:
            break  

    return max_value, best_move

def minimize_value(board, player, alpha, beta, available_moves):
    min_value = float('inf')
    best_move = None

    for move in available_moves:
        new_value, _ = evaluate_move(board, player, move, alpha, beta, True, available_moves)
        if new_value < min_value:
            min_value, best_move = new_value, move
        beta = min(beta, min_value)
        if beta <= alpha:
            break  

    return min_value, best_move

def evaluate_move(board, player, move, alpha, beta, is_maximizing, available_moves):
    new_board = make_move(board, move, player)
    new_state = [new_board, get_opponent(player)]
    return alpha_beta_pruning(new_state, alpha, beta, is_maximizing, available_moves)

