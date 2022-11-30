from board import Game, Board, Move
from player import Point, Player
import os

def print_board(board):
    for i in range(board):
        for j in range(board - i):
            print(" ")
            j += 1
        for k in range(2 * i - 1):
            if k == 0 or k == 2 * i - 2:
                print("*")
            else:
                print(" ")
            k += 1
        print("\n")
        i += 1

def main():
    red = Player.red
    blue = Player.blue
    green = Player.green
    yellow = Player.yellow
    orange = Player.orange
    pink = Player.pink
    while True:

        board_size = input("Please select board size (6/7/9): ")
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
    while not game.is_over():
        game.board.print()
        if game.next_player == red:
            while True:
                try:
                    human_row, human_col = input('Enter your move: ').split()
                    break
                except (ValueError):
                    print("Invalid Input, Try again")
            point = Point(int(human_row), int(human_col))
            move = Move(point)
        else:
            print("No")
        game = game.apply_move(move)
        os.system('clear')
        # move = bot.move(game)
        # game = game.apply_move(move)
    game.board.print()
    winner = game.winner()
    if winner is not None:
        print(winner, " is the winner ")



if __name__ == "__main__":
    main()