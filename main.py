from board import Game, Board
from player import Point, Player

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
        break

    winner = game.winner()
    if winner is not None:
        print(winner, " is the winner ")

    game.board.print()



if __name__ == "__main__":
    main()