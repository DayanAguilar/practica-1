# Define the player colors
BLACK = 'B'
WHITE = 'W'
EMPTY = ' '


def traduction_move(move):
    col = ord(move[0]) - ord('A')
    row = int(move[1]) - 1
    direction = move[3:]
    return row, col, direction


def get_opponent(player):
    if player == BLACK:
        return WHITE
    else:
        return BLACK


def move_northwest(new_board, row_copy, col_copy, previous_position, player):
    for n in range(1, min(row_copy + 1, col_copy + 1) + 1):
        if row_copy - n >= 0 and col_copy >= 0:
            if new_board[row_copy - n][col_copy - n] is not None:
                break
            new_board[row_copy - n][col_copy - n] = player
            new_board[previous_position[0]][previous_position[1]] = None
            previous_position = [row_copy - n, col_copy - n]
    return new_board

def move_north(new_board, row_copy, col_copy, previous_position, player):
    for n in range(1, row_copy + 1):
        if row_copy - n >= 0:
            if new_board[row_copy - n][col_copy] is not None:
                break
            new_board[row_copy - n][col_copy] = player
            new_board[previous_position[0]][previous_position[1]] = None
            previous_position = [row_copy - n, col_copy]
    return new_board

def move_northeast(new_board, row_copy, col_copy, previous_position, player):
    for n in range(1, min(row_copy + 1, 4 - col_copy) + 1):
        if row_copy - n >= 0 and col_copy + n < 4:
            if new_board[row_copy - n][col_copy + n] is not None:
                break
            new_board[row_copy - n][col_copy + n] = player
            new_board[previous_position[0]][previous_position[1]] = None
            previous_position = [row_copy - n, col_copy + n]
    return new_board

def move_west(new_board, row_copy, col_copy, previous_position, player):
    for n in range(1, col_copy + 1):
        if col_copy - n >= 0:
            if new_board[row_copy][col_copy - n] is not None:
                break
            new_board[row_copy][col_copy - n] = player
            new_board[previous_position[0]][previous_position[1]] = None
            previous_position = [row_copy, col_copy - n]
    return new_board

def move_east(new_board, row_copy, col_copy, previous_position, player):
    for n in range(1, 4 - col_copy):
        if col_copy + n < 4:
            if new_board[row_copy][col_copy + n] is not None:
                break
            new_board[row_copy][col_copy + n] = player
            new_board[previous_position[0]][previous_position[1]] = None
            previous_position = [row_copy, col_copy + n]
    return new_board

def move_southwest(new_board, row_copy, col_copy, previous_position, player):
    for n in range(1, min(4 - row_copy, col_copy + 1) + 1):
        if row_copy + n < 4 and col_copy - n >= 0:
            if new_board[row_copy + n][col_copy - n] is not None:
                break
            new_board[row_copy + n][col_copy - n] = player
            new_board[previous_position[0]][previous_position[1]] = None
            previous_position = [row_copy + n, col_copy - n]
    return new_board

def move_south(new_board, row_copy, col_copy, previous_position, player):
    for n in range(1, 4 - row_copy):
        if row_copy + n < 4:
            if new_board[row_copy + n][col_copy] is not None:
                break
            new_board[row_copy + n][col_copy] = player
            new_board[previous_position[0]][previous_position[1]] = None
            previous_position = [row_copy + n, col_copy]
    return new_board

def move_southeast(new_board, row_copy, col_copy, previous_position, player):
    for n in range(1, min(4 - row_copy, 4 - col_copy) + 1):
        if row_copy + n < 4 and col_copy + n < 4:
            if new_board[row_copy + n][col_copy + n] is not None:
                break
            new_board[row_copy + n][col_copy + n] = player
            new_board[previous_position[0]][previous_position[1]] = None
            previous_position = [row_copy + n, col_copy + n]
    return new_board

def directions_to_move(direction, new_board, row_copy, col_copy, previous_position, player):
    if direction == 'NW':
        return move_northwest(new_board, row_copy, col_copy, previous_position, player)
    elif direction == 'N':
        return move_north(new_board, row_copy, col_copy, previous_position, player)
    elif direction == 'NE':
        return move_northeast(new_board, row_copy, col_copy, previous_position, player)
    elif direction == 'W':
        return move_west(new_board, row_copy, col_copy, previous_position, player)
    elif direction == 'E':
        return move_east(new_board, row_copy, col_copy, previous_position, player)
    elif direction == 'SW':
        return move_southwest(new_board, row_copy, col_copy, previous_position, player)
    elif direction == 'S':
        return move_south(new_board, row_copy, col_copy, previous_position, player)
    elif direction == 'SE':
        return move_southeast(new_board, row_copy, col_copy, previous_position, player)
    else:
        return new_board

def make_move(board, move, player):
    row, col, direction = traduction_move(move)
    row_copy, col_copy = row, col
    previous_position = [row_copy, col_copy]

    if row_copy < 0 or row_copy > 3 or col_copy < 0 or col_copy > 3:
        raise ValueError(
            "Invalid move: position out of range ")

    new_board = [row[:] for row in board]

    return directions_to_move(direction, new_board, row_copy, col_copy, previous_position, player)


def forms_corners(board, player):

    corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
    for corner in corners:
        if board[corner[0]][corner[1]] != player:
            return False
    return True

def check_square(board, player, row, col):
    return (
        board[row][col] == player and
        board[row][col + 1] == player and
        board[row + 1][col] == player and
        board[row + 1][col + 1] == player
    )

def forms_square(board, player):
    for i in range(3):
        for j in range(3):
            if check_square(board, player, i, j):
                return True

    diagonal_positions = [
        (0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)
    ]
    for row, col in diagonal_positions:
        if board[row][col] == player and board[row + 1][col + 1] == player and \
           board[row][col + 1] == player and board[row + 1][col] == player:
            return True

    return False
