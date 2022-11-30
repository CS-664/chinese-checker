import random 
from player import Player

MAX_SCORE = 100
MIN_SCORE = -100
DRAW_SCORE = 1

def alphabeta_result(game_state, best_x, best_o):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE
        elif game_state.winner() == game_state.next_player.other:
            return MIN_SCORE
        else:
            return DRAW_SCORE
    
    best_result = MIN_SCORE
    for move in game_state.potential_moves():
        next_state = game_state.apply_move(move)
        opponent_result = alphabeta_result(next_state, best_x, best_o)
        my_result = -1 * opponent_result
        if my_result > best_result:
            best_result = my_result
        if game_state.next_player == Player.o:
            if best_result > best_o:
                best_o = best_result
            result_x = -1 * best_result
            if result_x < best_x:
                return best_result
        elif game_state.next_player == Player.x:
            if best_result > best_x:
                best_x = best_result
            result_o = -1 * best_result
            if result_o < best_o:
                return best_result
    return best_result

class AlphaBetaAgent():
    def move(self, game_state):
        best_moves = []
        best_score = None 
        best_x = MIN_SCORE
        best_o = MIN_SCORE

        for move in game_state.potential_moves():
            next_state = game_state.apply_move(move)
            opponent_result = alphabeta_result(next_state, best_x, best_o)
            my_result = -1 * opponent_result
            if not best_moves or my_result > best_score:
                best_moves = [move]
                best_score = my_result
                if game_state.next_player == Player.x:
                    best_x = best_score
                elif game_state.next_player == Player.o:
                    best_o = best_score
            elif my_result == best_score:
                best_moves.append(move)
        return random.choice(best_moves)