import enum
from collections import namedtuple

__all__ = [
    'Player',
    'Point',
    'Piece'
]
class Player(enum.Enum):
    red = 1
    blue = 2
    green = 3
    yellow = 4
    orange = 5
    pink = 6

    @property 
    def next(self):
        return Player.red if self == Player.pink else Player(self.value+1)
class Piece(enum.Enum):
    red = 1
    blue = 2
    green = 3
    yellow = 4
    orange = 5
    pink = 6

class Point(namedtuple('Point', 'row col')):
    def __deepcopy__(self, memodict={}):
        return self