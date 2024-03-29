from player import Player,Point,Piece
import copy
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
        if x - 1 >= 0 and x < self.size:
            neighbor.append(Point(x - 1, y))
            if y + 1 < self.size:
                neighbor.append(Point(x, y + 1))
                neighbor.append(Point(x - 1, y + 1))

        if x + 1 < self.size:
            neighbor.append(Point(x + 1, y))
            if y - 1 >= 0 and y < self.size:
                neighbor.append(Point(x, y - 1))
                neighbor.append(Point(x + 1, y - 1))

        if y + 1 < self.size:
            neighbor.append(Point(x, y + 1))
            if x - 1 >= 0 and x < self.size:
                neighbor.append(Point(x - 1, y))
                neighbor.append(Point(x - 1, y + 1))

        if y - 1 >= 0 and y < self.size:
            neighbor.append(Point(x, y - 1))
            if x + 1 < self.size:
                neighbor.append(Point(x + 1, y))
                neighbor.append(Point(x + 1, y - 1))

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
        return neighbor
    
    #check if point is on board
    def is_on_board(self, point):
        if point.row < 0 or point.col < 0 or point.row >= self.board_size or point.col >= self.board_size:
            return False
        else:
            return True

    
    def get(self, point):
        return self.board.get(point)
    
    def update(self, point, value):
        self.board.update({point:value})
    
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
        if move is None:
            return Game(self.board, self.next_player.other, None, self.num)
        next_board = copy.deepcopy(self.board)
        next_board.update(move.end_point, next_board.get(move.start_point))
        next_board.update(move.start_point, None)              # update board information                                      # re-print new game board
        return Game(next_board,self.next_player.other,move,self.num)

    
    #return if the move is legal
    def is_valid_move(self, move, s):
        if move.end_point.row < 0 or move.end_point.row >= self.board.size or move.end_point.col < 0 or move.end_point.col >= self.board.size:  # if end point out of the board
            return False
        elif self.board.get(move.end_point) is not None:       # if there has already had a piece on the end point
            return False
        elif self.board.get(move.end_point) is None:
            if s is None:
                start = move.start_point
            else:
                start = s
            if self.board.get(start) == Piece.red:
                start_depth = move.start_point.row + move.start_point.col
                end_depth = move.end_point.row + move.end_point.col
                if end_depth < start_depth:
                    return False
                else:
                    return True
            if self.board.get(start) == Piece.blue:
                start_depth = move.start_point.row + move.start_point.col
                end_depth = move.end_point.row + move.end_point.col
                if end_depth > start_depth:
                    return False
                else:
                    return True
        else:
            return True
    
    def jump(self, start_point, current_point, jumped):
        moves = []
        for middle_point in self.board.neighbor(current_point.row, current_point.col):
            if self.board.get(middle_point) is None:
                continue
            sx, sy, mx, my = current_point.row, current_point.col, middle_point.row, middle_point.col 
            if sx - 1 == mx and sy == my: # upper 
                end_point = Point(sx-2,sy)
            elif sx - 1 == mx and sy + 1 == my: # upper-right
                end_point = Point(sx-2,sy+2)
            elif sx == mx and sy + 1 == my: #right
                end_point = Point(sx, sy+2)
            elif sx + 1 == mx and sy == my: #bottom
                end_point = Point(sx+2, sy)
            elif sx + 1 == mx and sy - 1 == my: #bottom-left
                end_point = Point(sx+2, sy-2)
            elif sx == mx and sy - 1 == my: #left
                end_point = Point(sx, sy-2)
            if self.is_valid_move(Move(current_point, end_point),start_point):
                if end_point not in jumped:
                    jumped.append(current_point)
                    moves.append(Move(start_point, end_point))
                    moves.extend(self.jump(start_point,end_point,jumped))
        return moves

    #return list of potential move of current player
    def potential_moves(self):
        moves= []
        for p in self.board.get_all_pieces(self.next_player.value):
            for neighbor in self.board.neighbor(p.row, p.col):
                #print("{} to {} is {}".format(p, neighbor, self.is_valid_move(Move(p, neighbor))))
                if self.is_valid_move(Move(p, neighbor),None):
                    moves.append(Move(p, neighbor))
            jump_moves = self.jump(p,p,[])
            for jump_move in jump_moves:
                if self.is_valid_move(jump_move,None):
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
        if self.board.size == 6:
            cRed = {Point(5,5),Point(4,5),Point(3,5),Point(5,4),Point(4,4),Point(5,3)}
            cBlue = {Point(0,0),Point(0,1),Point(0,2),Point(1,0),Point(1,1),Point(2,0)}
            if player == Player.red:
                for point in cRed:
                    if self.board.get(point) == Piece.red:
                        cWin = True
                    else:
                        cWin = False
                        break
            else:
                for point in cBlue:
                    if self.board.get(point) == Piece.blue:
                        cWin = True
                    else:
                        cWin = False
                        break
        if self.board.size == 7:
            cRed = {Point(6, 6), Point(5, 6), Point(4, 6), Point(6, 5), Point(5, 5), Point(6, 4)}
            cBlue = {Point(0, 0), Point(0, 1), Point(0, 2), Point(1, 0), Point(1, 1), Point(2, 0)}
            if player == Player.red:
                for point in cRed:
                    if self.board.get(point) == Piece.red:
                        cWin = True
                    else:
                        cWin = False
                        break
            else:
                for point in cBlue:
                    if self.board.get(point) == Piece.blue:
                        cWin = True
                    else:
                        cWin = False
                        break
        if self.board.size == 9:
            cRed = {Point(8, 8), Point(7, 8), Point(6, 8), Point(8, 7), Point(7, 7), Point(8, 6)}
            cBlue = {Point(0, 0), Point(0, 1), Point(0, 2), Point(1, 0), Point(1, 1), Point(2, 0)}
            if player == Player.red:
                for point in cRed:
                    if self.board.get(point) == Piece.red:
                        cWin = True
                    else:
                        cWin = False
                        break
            else:
                for point in cBlue:
                    if self.board.get(point) == Piece.blue:
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
