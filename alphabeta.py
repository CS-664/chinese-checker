import random 
from player import Player
from board import *

MAX_SCORE = 10000
MIN_SCORE = -10000
DEPTH = 3

def cal_score(game_state, player):
    score = 0
    bias_fine = 0.2
    last_chess_fine = 0.5
    last_chess = 0 
    for p in game_state.board.get_all_pieces(player.value):
        if player == Player.red:
            layer = p.row + p.col #what layer is p in
            if last_chess < 10 - layer:
                last_chess = 10 - layer
            score += layer - bias_fine * abs(p.row - p.col)
        else:
            layer = p.row + p.col
            last_chess = max(last_chess, layer)
            score += (10-layer) - bias_fine * abs(p.row - p.col)
    score += 60 + bias_fine * 7 - last_chess_fine * last_chess 
        
    return score



class AlphaBetaAgent():
    def __init__(self, piece):
        self.player = piece
    def move(self, game_state):
        best_moves = []
        best_score = None 
        alpha = MIN_SCORE
        beta = MAX_SCORE

        for move in game_state.potential_moves():
            next_state = game_state.apply_move(move)
            score = self.alphabeta_result(next_state, DEPTH, alpha, beta)
            if score == MAX_SCORE:
                return move
            if not best_moves or score > best_score:
                best_moves = [move]
                best_score = score
            elif score == best_score:
                best_moves.append(move)
        if len(best_moves) == 0:
            return None
        return random.choice(best_moves)
    
    def alphabeta_result(self, game_state, depth, alpha, beta):
        if game_state.is_over():
            if game_state.winner() == self.player:
                return MAX_SCORE

        
        if depth == 0:
            return cal_score(game_state, self.player)

        if game_state.next_player != self.player:
            for move in game_state.potential_moves():
                next_state = game_state.apply_move(move)
                score = self.alphabeta_result(next_state, depth-1, alpha, beta)
                if score < beta:
                    beta = score
                    if alpha >= beta:
                        return alpha
            return beta 
        else:
            for move in game_state.potential_moves():
                next_state = game_state.apply_move(move)
                score = self.alphabeta_result(next_state, depth-1, alpha, beta)
                if score >= alpha:
                    alpha = score
                    if alpha >= beta:
                        return beta
            return alpha

