from player import Player
__all__ = [
    'Board',
    'Game',
]

class Board:
    def __init__(self, board_size, num):
        self.board = []
        self.num = num

class Game:
    def __init__(self, board, next_player, move, num):
        self.board = board
        self.next_player = next_player
        self.last_move = move
        self.num = num 
    
    def new_game(board_size, num):
        board = Board(board_size, num)
        return Game(board, Player.red, None, num)
