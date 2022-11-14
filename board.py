from player import Player,Point,Piece
__all__ = [
    'Board',
    'Game',
]

class Board:
    def __init__(self, board_size, num):
        self.board = {}
        self.size = board_size
        self.num = num
        if num == 2:
            for i in range(board_size):
                for j in range(board_size):
                    point = Point(i,j)
                    if (i == 0 and (j == 0 or j == 1 or j == 2)) or \
                       (i == 1 and (j == 0 or j == 1)) or \
                       (i == 2 and j ==0):
                        self.board[point] = Piece.red
                    elif (i == board_size - 3 and j == board_size - 1) or \
                         (i == board_size -2 and (j == board_size - 1 or j == board_size -2)) or \
                         (i == board_size -1 and (j == board_size - 1 or j == board_size -2 or j == board_size - 3)):
                        self.board[point] = Piece.blue
                    else:
                        self.board[point] = None

    def print(self):
        zigzag = []
        for line in range(1,2*self.size):
            start_col = max(0, line - self.size)
            count = min(line, (self.size - start_col), self.size)
            for j in range(0, count):
                zigzag.append(self.board[Point(min(self.size, line) - j - 1,start_col + j)])
        rows = self.size - 1 
        k = 2 * rows - 2 
        counter = 0  
        for i in range(0, rows):                
            for j in range(0, k):  
                print(end=" ")   
            k = k - 1   
            for j in range(0, i + 1):
                if zigzag[counter] == Piece.red:
                    print("x ", end="")  
                elif zigzag[counter] == Piece.blue:
                    print("o ", end="")
                else:
                    print("* ", end="")
                counter += 1  
            print("")  

        k = rows - 2    
        for i in range(rows, -1, -1):   
            for j in range(k, 0, -1):  
                print(end=" ")  
            k = k + 1    
            for j in range(0, i + 1):  
                if zigzag[counter] == Piece.red:
                    print("x ", end="")  
                elif zigzag[counter] == Piece.blue:
                    print("o ", end="")
                else:
                    print("* ", end="")
                counter += 1    
            print("")


class Game:
    def __init__(self, board, next_player, move, num):
        self.board = board
        self.next_player = next_player
        self.last_move = move
        self.num = num 
    
    def new_game(board_size, num):
        board = Board(board_size, num)
        return Game(board, Player.red, None, num)
