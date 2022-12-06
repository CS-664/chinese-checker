from board import Game, Board, Move
from player import Point, Player
from alphabeta import AlphaBetaAgent

def main():
    game_num = 0
    total_round = 0
    win_num = 0
    loss_num = 0
    draw_num = 0
    while game_num <= 0:
        game = Game.new_game(6, 2)
        round = 0
        step = 0
        while not game.is_over():
            if step >= 250:
                draw_num += 1
                break
            round += 1
            step += 1
            total_round += 1
            game.board.print()
            alpha1 = AlphaBetaAgent()
            alpha2 = AlphaBetaAgent()
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
        
        print("Average step is {}, win_num is {}, draw_num is {}, loss_num is {}".format(total_round/game_num, win_num, draw_num, loss_num))
    
if __name__ == "__main__":
    main()