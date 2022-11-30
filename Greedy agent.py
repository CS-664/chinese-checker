from player import *
from board import *
import enum

class GameResult(enum.Enum):
    rWin = 1
    bWin = 2
    gWin = 3
    yWin = 4
    oWin = 5
    pWin = 6

def best_move(game):
    if game.is_over():
        if game.check_win(red):