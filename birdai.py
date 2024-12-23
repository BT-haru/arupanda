import math
import random

BLACK = 1
WHITE = 2
INF = math.inf

def evaluate_board(board, stone):
    """
    改良された評価関数。盤面の状態を数値化する。
    """
    opponent = 3 - stone
    score = 0

    # フェーズの判定
    empty_squares = sum(row.count(0) for row in board)
    early_game = empty_squares > 30
    mid_game = 15 < empty_squares <= 30
    late_game = empty_squares <= 15

    # 角の評価
    corners = [(0, 0), (0, 5), (5, 0), (5, 5)]
    for x, y in corners:
        if board[y][x] == stone:
            score += 100
        elif board[y][x] == opponent:
            score -= 100

    # 安定石の評価（動かせない石）
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone and is_stable(board, x, y, stone):
                score += 20
            elif board[y][x] == opponent and is_stable(board, x, y, opponent):
                score -= 20

    # モビリティ（合法手の数）
    mobility = len(get_possible_moves(board, stone))
    opponent_mobility = len(get_possible_moves(board, opponent))
    score += (mobility - opponent_mobility) * (15 if early_game else 5)

    # 終盤は石の数を重視
    if late_game:
        player_count = sum(row.count(stone) for row in board)
        opponent_count = sum(row.count(opponent) for row in board)
        score += (player_count - opponent_count) * 10

    return score

def is_stable(board, x, y, stone):
    """
    石が安定しているか（動かされる可能性がないか）を判定。
    """
    if board[y][x] != stone:
        return False
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board):
            if board[ny][nx] == 0:
                return False
            nx += dx
            ny += dy
    return True

def can_place_x_y(board, stone, x, y):
    if board[y][x] != 0:
        return False
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True

    return False

def get_possible_moves(board, stone):
    moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                moves.append((x, y))
    return moves

def minimax(board, depth, alpha, beta, maximizing_player, stone):
    possible_moves = get_possible_moves(board, stone)
    opponent = 3 - stone

    if depth == 0 or not possible_moves:
        return evaluate_board(board, stone)

    if maximizing_player:
        max_eval = -INF
        for move in possible_moves:
            x, y = move
            board[y][x] = stone
            eval = minimax(board, depth - 1, alpha, beta, False, stone)
            board[y][x] = 0
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = INF
        for move in possible_moves:
            x, y = move
            board[y][x] = opponent
            eval = minimax(board, depth - 1, alpha, beta, True, stone)
            board[y][x] = 0
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(board, stone):
    best_value = -INF
    best_move = None
    possible_moves = get_possible_moves(board, stone)

    for move in possible_moves:
        x, y = move
        board[y][x] = stone
        move_value = minimax(board, 6 if len(get_possible_moves(board, stone)) < 10 else 4, -INF, INF, False, stone)
        board[y][x] = 0

        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move

class birdAI:
    def face(self):
        return "🦉"

    def place(self, board, stone):
        return best_move(board, stone)
