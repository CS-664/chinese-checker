from player import Player,Point,Piece
__all__ = [
    'Board',
    'Game',
    'Move',
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
    def neibor(self,x,y):
        neibor = []
        if x - 1 >=0 :
            neibor.append([x - 1, y])
            if y - 1 >= 0:
                neibor.append([x, y - 1])
                neibor.append([x - 1, y - 1])

        if x + 1 <= self.size:
            neibor.append([x + 1, y])
            if y + 1 <= self.size:
                neibor.append([x, y+1])
                neibor.append([x + 1, y + 1])

        if y + 1 <= self.size:
            neibor.append([x, y+1])
            if x + 1 <= self.size:
                neibor.append([x + 1, y])
                neibor.append([x + 1, y + 1])

        if y - 1 >= 0:
            neibor.append([x, y - 1])
            if x - 1 >= 0:
                neibor.append([x - 1, y])
                neibor.append([x - 1, y - 1])
            neibor.append([x - 1, y - 1])
        neibor.sort()

        length = len(neibor)
        last = neibor[length - 1]
        for i in range(length - 2, -1, -1):
            now = neibor[i]
            if now == last:
                neibor.remove(now)
            else:
                last = now
        return neibor
    #check if the move is legal
    def check_move(self, player, start_point, end_point):
        curMove = Move(start_point,end_point)
        if player == Player.red:
            if curMove.end_point.row < curMove.start_point.row or curMove.end_point.col < curMove.start_point.col:
                return False
        if player == Player.blue:
            if curMove.end_point.row > curMove.start_point.row or curMove.end_point.col > curMove.start_point.col:
                return False
        # add if for other player if we need

        return Game.is_valid_move(curMove)
    
    #check if point is on board
    def is_on_board(self, point):
        if point.row < 0 or point.col < 0 or point.row >= self.board_size or point.col >= self.board_size:
            return False
        else:
            return True
        #return 0
    
    def get(self, point):
        return self.board.get(point)

class Move:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

class Game:
    def __init__(self, board, next_player, move, num):
        self.board = board
        self.next_player = next_player
        self.last_move = move
        self.num = num 
    
    def new_game(board_size, num):
        board = Board(board_size, num)
        return Game(board, Player.red, None, num)
    
    # return game status after the move 
    def apply_move(self, move):
        Board.board[move.end_point] = Board.board[move.start_point]
        Board.board[move.start_point] = None               # update board information
        Board.print()                                      # re-print new game board
        return self.is_over()               # return game status if it's end or not


    
    #return if the move is legal
    def is_valid_move(self, move):
        if move.end_point.row < 0 or move.end_point.row >= Board.size or move.end_point.col < 0 or move.end_point.col >= Board.size:  # if end point out of the board
            return False
        elif self.board[move.end_point] is not None:       # if there has already had a piece on the end point
            return False
        else:
            return True
    
    #return list of potential move of current player
    def potential_move(self):
        return 0
    
    #check if game is over
    def is_over(self):
        if self.check_win(Player.red) or self.check_win(Player.blue) or self.check_win(Player.green) or self.check_win(
                Player.yellow) or self.check_win(Player.orange) or self.check_win(Player.pink):
            return True
        return False

    #check if there is winner
    def check_win(self, player):
        Cred = []      # list to check if red win the game
        Cblue = []     # list to check if blue win the game
        Cgreen = []
        Cyellow = []
        Corange = []
        Cpink = []
        cWin = False      # return if target player win the game or not
        for i in range(self.board_size):
            for j in range(self.board_size):
                point = Point(i, j)
                if self.board[point] == Piece.red:
                    Cblue.append(point)
                if self.board[point] == Piece.blue:
                    Cred.append(point)
                # if.....     add code here for other players if we need
        if player == Player.red:
            for k in range(len(Cred)):
                if self.board[Cred[k]] == Piece.red:
                    cWin = True
                else:
                    cWin = False
                    break
        if player == Player.blue:
            for k in range(len(Cblue)):
                if self.board[Cblue[k]] == Piece.blue:
                    cWin = True
                else:
                    cWin = False
                    break
        # add if here for other player if we need


        return cWin


        
    #return winner
    def winner(self):
        if self.check_win(Player.red):
            return Player.red
        if self.check_win(Player.blue):
            return Player.blue
        if self.check_win(Player.green):
            return Player.green
        if self.check_win(Player.yellow):
            return Player.yellow
        if self.check_win(Player.orange):
            return Player.orange
        if self.check_win(Player.pink):
            return Player.pink
        return None
