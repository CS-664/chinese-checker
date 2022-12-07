import random 

class RandomBot():
    def move(self, game):
        moves = game.potential_moves()
        if len(moves) == 0:
            return None
        return random.choice(moves)