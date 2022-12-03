import random 
from player import Player
from board import *

MAX_SCORE = 10000
MIN_SCORE = -10000
DEPTH = 5

def alphabeta(game_state, depth, alpha, beta):
        if game_state.is_over():
            if game_state.winner() == Player.red:
                return MAX_SCORE, game_state.last_move
            else:
                return MIN_SCORE, game_state.last_move
        if depth == 0:
            score = cal_score(game_state)
            return score, None
        
        scores = []
        moves = []
        if game_state.next_player == Player.red:
            for move in game_state.potential_moves():
                next_state = game_state.apply_move(move)
                (score, next_move) = alphabeta(game_state, depth - 1, alpha, beta)
                scores.append(score)
                moves.append(move)
                alpha = max(score, alpha)
                if beta <= alpha:
                    break 
            if len(scores) == 0:
                return 0, None
            max_score_index = scores.index(max(scores))
            best_move = moves[max_score_index]
            return scores[max_score_index], best_move
        else:
            for move in game_state.potential_moves():
                next_state = game_state.apply_move(move)
                score, next_move = alphabeta_result(game_state, depth - 1, alpha, beta)
                scores.append(score)
                moves.append(move)
                beta = min(score, beta)
                if beta <= alpha:
                    break 
            if len(scores) == 0:
                return 0, None
            min_score_index = scores.index(min(scores))
            worst_move = moves[min_score_index]
            return scores[min_score_index], worst_move

def cal_score(game_state):
    score = 1000
    target_layer = 0
    if game_state.next_player.value == Player.red:
        target_layer = 10
    else:
        target_layer = 0
    for p in game_state.board.get_all_pieces(game_state.next_player.value):
        layer = p.row + p.col #what layer is p in
        score -= abs(layer - target_layer)
    return score


def alphabeta_result(game_state, depth, alpha, beta):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE
        else:
            return MIN_SCORE
    
    if depth <= 0:
        return cal_score(game_state)

    if game_state.next_player == Player.blue:
        for move in game_state.potential_moves():
            next_state = game_state.apply_move(move)
            score = alphabeta_result(next_state, depth-1, alpha, beta)
            if score < beta:
                beta = score
                if alpha >= beta:
                    return alpha
        return beta 
    else:
        for move in game_state.potential_moves():
            next_state = game_state.apply_move(move)
            score = alphabeta_result(next_state, depth-1, alpha, beta)
            if score >= alpha:
                alpha = score
                if alpha >= beta:
                    return beta
        return alpha
    '''
    for move in game_state.potential_moves():
        next_state = game_state.apply_move(move)
        score = alphabeta_result(next_state, depth-1, alpha, beta)
        if score > best_result:
            best_result = score
        if game_state.next_player == Player.red:
            if best_result > beta:
                beta = best_result
            result_me = -1 * best_result
            if result_me < alpha:
                return best_result
        elif game_state.next_player == Player.blue:
            if best_result > alpha:
                alpha = best_result
            result_op = -1 * best_result
            if result_op < beta:
                return best_result
    return best_result
    '''

class AlphaBetaAgent():
    def move1(self, game_state):
        best_moves = []
        best_score = None 
        alpha = MIN_SCORE
        beta = MIN_SCORE

        for move in game_state.potential_moves():
            next_state = game_state.apply_move(move)
            score = alphabeta_result(game_state, DEPTH, alpha, beta)
            if not best_moves or score > best_score:
                best_moves = [move]
                best_score = score
                if game_state.next_player == Player.red:
                    alpha = best_score
                elif game_state.next_player == Player.blue:
                    beta = best_score
            elif score == best_score:
                best_moves.append(move)
        return random.choice(best_moves)

    def move(self, game_state):
        alpha = MIN_SCORE
        beta = MIN_SCORE
        (scores, best_move) = alphabeta(game_state, DEPTH, alpha, beta)
        return best_move
