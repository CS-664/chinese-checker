from board import Game, Board

def main():
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
    game.board.print()



if __name__ == "__main__":
    main() 