import math
import random

BLACK=1
WHITE=2

board = [
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,1,2,0,0],
        [0,0,2,1,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
]

def can_place_x_y(board, stone, x, y):
    """
    石を置けるかどうかを調べる関数。
    board: 2次元配列のオセロボード
    x, y: 石を置きたい座標 (0-indexed)
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    return: 置けるなら True, 置けないなら False
    """
    if board[y][x] != 0:
        return False  # 既に石がある場合は置けない

    opponent = 3 - stone  # 相手の石 (1なら2、2なら1)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True  # 石を置ける条件を満たす

    return False

def can_place(board, stone):
    """
    石を置ける場所を調べる関数。
    board: 2次元配列のオセロボード
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    """
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                return True
    return False

def random_place(board, stone):
    """
    石をランダムに置く関数。
    board: 2次元配列のオセロボード
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    """
    while True:
        x = random.randint(0, len(board[0]) - 1)
        y = random.randint(0, len(board) - 1)
        if can_place_x_y(board, stone, x, y):
            return x, y

def possible_moves(board, stone):
    """
    現在のボードで置けるすべての座標を返す関数。
    """
    moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                moves.append((x, y))
    return moves

def simulate_move(board, stone, x, y):
    """
    ボードをコピーして、指定の座標に石を置いた後のボードを返す。
    """
    new_board = [row[:] for row in board]  # ボードをコピー
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    opponent = 3 - stone

    new_board[y][x] = stone

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        stones_to_flip = []

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board):
            if new_board[ny][nx] == opponent:
                stones_to_flip.append((nx, ny))
            elif new_board[ny][nx] == stone:
                for flip_x, flip_y in stones_to_flip:
                    new_board[flip_y][flip_x] = stone
                break
            else:
                break
            nx += dx
            ny += dy

    return new_board


class PandaAI(object):

    def face(self):
        return "🐇"

    def place(self, board, stone):
        x, y = random_place(board, stone)
        return x, y

class AruAI(PandaAI):#ww
    def __init__(self, simulations=100):
        self.simulations = simulations  # 1手につき行うシミュレーションの回数

    def simulate_game(self, board, stone):
        """
        現在の盤面から終局までランダムにゲームを進め、結果を返す。
        stone: シミュレーション開始時のプレイヤーの石
        """
        sim_board = [row[:] for row in board]  # ボードをコピー
        current_stone = stone

        while can_place(sim_board, BLACK) or can_place(sim_board, WHITE):
            if can_place(sim_board, current_stone):
                x, y = random_place(sim_board, current_stone)
                sim_board = simulate_move(sim_board, current_stone, x, y)
            current_stone = 3 - current_stone  # プレイヤー交代

        # 終局後のスコアを計算
        black_score = sum(row.count(BLACK) for row in sim_board)
        white_score = sum(row.count(WHITE) for row in sim_board)

        # 勝敗を返す
        if stone == BLACK:
            return 1 if black_score > white_score else -1 if black_score < white_score else 0
        else:
            return 1 if white_score > black_score else -1 if white_score < black_score else 0

    def place(self, board, stone):
        """
        モンテカルロ法を使って最適な手を選ぶ。
        """
        moves = possible_moves(board, stone)
        if not moves:
            return random_place(board, stone)  # 合法手がない場合はランダム

        move_scores = {move: 0 for move in moves}

        # 各手についてシミュレーション
        for move in moves:
            for _ in range(self.simulations):
                sim_board = simulate_move(board, stone, move[0], move[1])
                result = self.simulate_game(sim_board, stone)
                move_scores[move] += result

        # 最もスコアが高い手を選ぶ
        best_move = max(move_scores, key=move_scores.get)
        return best_move
