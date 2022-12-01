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

    def neighbor(self,x,y):
        neighbor = []
        if x - 1 >0 and x < self.size:
            neighbor.append(Point(x - 1, y))
            if y - 1 > 0 and y < self.size:
                neighbor.append(Point(x, y - 1))
                neighbor.append(Point(x - 1, y - 1))

        if x + 1 < self.size:
            neighbor.append(Point(x + 1, y))
            if y + 1 < self.size:
                neighbor.append(Point(x, y+1))
                neighbor.append(Point(x + 1, y + 1))

        if len(neighbor) > 1:
            neighbor.sort()
            length = len(neighbor)
            lastItem = neighbor[length - 1]
            for i in range(length - 2, -1, -1):
                currentItem = neighbor[i]
                if currentItem == lastItem:
                    neighbor.remove(currentItem)
                else:
                    lastItem = currentItem
        print("{} {} neighbors are {}".format(x, y, neighbor))
        return neighbor
    
    #check if point is on board
    def is_on_board(self, point):
        if point.row < 0 or point.col < 0 or point.row >= self.board_size or point.col >= self.board_size:
            return False
        else:
            return True

    
    def get(self, point):
        return self.board.get(point)
    
    #Return Point
    def get_all_pieces(self, piece):
        pieces = []
        for i in range(self.size):
            for j in range(self.size):
                if self.get(Point(i,j)) is not None and self.get(Point(i,j)).value == piece:
                    pieces.append(Point(i,j))
        return pieces

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
        return Game(self.board,self.next_player,move,self.num)

    
    #return if the move is legal
    def is_valid_move(self, move):
        if move.end_point.row < 0 or move.end_point.row >= self.board.size or move.end_point.col < 0 or move.end_point.col >= self.board.size:  # if end point out of the board
            return False
        elif self.board.get(move.end_point) is not None:       # if there has already had a piece on the end point
            return False
        elif self.board.get(move.end_point) is None:
            if self.board.get(move.start_point) == Piece.red:
                if move.end_point.col < move.start_point.col:
                    return False
            if self.board.get(move.start_point) == Piece.blue:
                if move.end_point.col > move.start_point.col:
                    return False
        else:
            return True
    
    def jump(self, start_point):
        moves = []
        for middle_point in self.board.neighbor(start_point.row, start_point.col):
            if self.board.get(middle_point) is None:
                continue
            sx, sy, mx, my = start_point.row, start_point.col, middle_point.row, middle_point.col 
            if sx - 1 == mx and sy == my: # upper 
                end_point = Point(sx-2,sy)
            elif sx - 1 == mx and sy + 1 == my: # upper-right
                end_point = Point(sx-2,sy+2)
            elif sx == mx and sy + 1 == my: #right
                end_point = Point(sx, sy+2)
            elif sx + 1 == mx and sy == my: #bottom
                end_point = Point(sx+2, sy)
            elif sx + 1 == mx and sy - 1 == mx: #bottom-left
                end_point = Point(sx+2, sy-2)
            elif sx == my and sy - 1 == my: #left
                end_point = Point(sx, sy-2)
            if self.is_valid_move(Move(start_point, end_point)):
                moves.append(Move(start_point, end_point))
                moves.extend(self.jump(end_point))
        return moves

    #return list of potential move of current player
    def potential_moves(self):
        moves= []
        for p in self.board.get_all_pieces(self.next_player.value):
            start_point = p
            for neighbor in self.board.neighbor(p.row, p.col):
                if self.is_valid_move(Move(p, neighbor)):
                    moves.append(Move(p, neighbor))
            jump_moves = self.jump(p)
            for jump_move in jump_moves:
                if self.is_valid_move(jump_move):
                    moves.append(jump_move)
        return moves
    
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
        for i in range(self.board.size):
            for j in range(self.board.size):
                point = Point(i, j)
                if self.board.get(point) == Piece.red:
                    Cblue.append(point)
                if self.board.get(point) == Piece.blue:
                    Cred.append(point)
                if self.board.get(point) == Piece.yellow:
                    Cgreen.append(point)
                if self.board.get(point) == Piece.green:
                    Cyellow.append(point)
                if self.board.get(point) == Piece.pink:
                    Corange.append(point)
                if self.board.get(point) == Piece.orange:
                    Cpink.append(point)
        if player == Player.red:
            for k in range(len(Cred)):
                if self.board.get(Cred[k]) == Piece.red:
                    cWin = True
                else:
                    cWin = False
                    break
        if player == Player.blue:
            for k in range(len(Cblue)):
                if self.board.get(Cblue[k]) == Piece.blue:
                    cWin = True
                else:
                    cWin = False
                    break
        if player == Player.green:
            for k in range(len(Cgreen)):
                if self.board.get(Cgreen[k])== Piece.green:
                    cWin = True
                else:
                    cWin = False
                    break
        if player == Player.orange:
            for k in range(len(Corange)):
                if self.board.get(Corange[k]) == Piece.orange:
                    cWin = True
                else:
                    cWin = False
                    break
        if player == Player.yellow:
            for k in range(len(Cyellow)):
                if self.board.get(Cyellow[k]) == Piece.yellow:
                    cWin = True
                else:
                    cWin = False
                    break
        if player == Player.pink:
            for k in range(len(Cpink)):
                if self.board.get(Cpink[k]) == Piece.pink:
                    cWin = True
                else:
                    cWin = False
                    break


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
