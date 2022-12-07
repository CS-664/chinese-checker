from board import Game, Board, Move
from player import Point, Player
from alphabeta import AlphaBetaAgent
from randombot import RandomBot
from greedy import GreedyAgent
from mcts import MCTSAgent
import os
import time

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
    red = Player.red
    blue = Player.blue
    green = Player.green
    yellow = Player.yellow
    orange = Player.orange
    pink = Player.pink
    round = 0
    while True:

        board_size = '6'#input("Please select board size (6/7/9): ")
        if board_size == '6':
            game = Game.new_game(6, 2)
            break
        elif board_size == '7' or board_size == '9':
            player = input("Please select player number (1-5): ")
            if ord('1') <= ord(player) <= ord('5'):
                game = Game.new_game(int(board_size), int(player))
                break
            else:
                print("Illegal number of player, Try Again!")
                continue
        else:
            print("Illegal board size, Try Again!")
    while not game.is_over() and round <= 250:
        round += 1
        game.board.print()
        #time.sleep(1)
        alpha = MCTSAgent(1000, 0.5)
        silly = AlphaBetaAgent(Player.blue)
        if game.next_player == red:
            
            '''
            while True:
                try:
                    human_row, human_col = input('Enter your move: ').split()
                    break
                except (ValueError):
                    print("Invalid Input, Try again")
            point = Point(int(human_row), int(human_col))
            move = Move(point)
            '''
            move = alpha.move(game)
        else:
            move = silly.move(game)
        game = game.apply_move(move)
        os.system('clear')
        # move = bot.move(game)
        # game = game.apply_move(move)
    game.board.print()
    winner = game.winner()
    if winner is not None:
        print("{} is the winner in {} rounds".format(winner, round))
    else:
        red_score = cal_score(game, Player.red)
        blue_score = cal_score(game, Player.blue)
        print("{} is the winner".format(Player.red if red_score > blue_score else Player.blue))



if __name__ == "__main__":
    main()