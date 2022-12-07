from board import Game, Board, Move
from player import Point, Player
from alphabeta import AlphaBetaAgent

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
    
def main():
    game_num = 1
    total_round = 0
    win_num = 0
    loss_num = 0
    while game_num <= 100:
        game = Game.new_game(6, 2)
        round = 0
        step = 0
        step_num = 0
        while not game.is_over():
            if step >= 250:
                red_score = cal_score(game, Player.red)
                blue_score = cal_score(game, Player.blue)
                if red_score > blue_score:
                    win_num += 1
                else:
                    loss_num += 1
                total_round -= step
                step_num -= 1
                break
            round += 1
            step += 1
            total_round += 1
            game.board.print()
            alpha1 = AlphaBetaAgent(Player.red)
            alpha2 = AlphaBetaAgent(Player.blue)
            if game.next_player == Player.red:
                move = alpha1.move(game)
            else:
                move = alpha2.move(game)
            game = game.apply_move(move)
        winner = game.winner()
        if winner is not None:
            if winner == Player.red:
                win_num += 1
            else:
                loss_num += 1   
        if step_num != 0 and total_round != 0:   
            print("Average step is {}, win_num is {}, draw_num is {}, loss_num is {}".format(total_round/game_num, win_num, draw_num, loss_num))
        game_num += 1
        step_num += 1
    print("Average step is {}, win_num is {}, draw_num is {}, loss_num is {}".format(total_round/game_num, win_num, draw_num, loss_num))
    
if __name__ == "__main__":
    main()