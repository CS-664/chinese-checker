from player import Player
from board import *
import random 

DEPTH = 3
MIN_SCORE = -1000
MAX_SCORE = 1000
WINNING_BONUS = 2

def evaluation(game_state):
    score = 0
    bias_fine = 0.2
    last_chess_fine = 0.5
    last_chess = 0
    for p in game_state.board.get_all_pieces(Player.red.value):
        layer = p.row + p.col #what layer is p in
        if last_chess < 10 - layer:
            last_chess = 10 - layer
        score += layer - bias_fine * abs(p.row - p.col)
    score += 60 + bias_fine * 7 - last_chess_fine * last_chess 
        
    return score

def max_search(game_state, depth):
    best_score = MIN_SCORE
    if game_state.is_over():
        if game_state.winner() == Player.red:
            return MAX_SCORE
    if depth == 0:
        return evaluation(game_state)
    opponent_moves = game_state.potential_moves()
    if len(opponent_moves) == 0:
        game_state.board.print()
    opponent_move = random.choice(opponent_moves)
    my_turn = game_state.apply_move(opponent_move)
    for move in my_turn.potential_moves():
            next_state = game_state.apply_move(move)
            score = max_search(next_state, depth-1)
            if score > best_score:
                best_score = score
    return best_score
    
     
class MaxAgent():
    def move(self, game_state):
        best_score = MIN_SCORE
        best_move = None
        for move in game_state.potential_moves():
            next_state = game_state.apply_move(move)
            score = max_search(next_state, DEPTH)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
            