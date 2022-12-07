'''
    Shanghua Yang ysh99226@bu.edu
    Xiangyu Hu xyuhu@bu.edu
    Yilin Li lyl1021@bu.edu
    Jiaxin Chen chenjiax@bu.edu
'''

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
    game = Game.new_game(6, 2)
    while not game.is_over() and round <= 250:
        round += 1
        game.board.print()
        #time.sleep(1)
        agent1 = AlphaBetaAgent(Player.red, 3)
        agent2 = GreedyAgent()
        if game.next_player == red:
            move = agent1.move(game)
        else:
            move = agent2.move(game)
        game = game.apply_move(move)
        os.system('clear')
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