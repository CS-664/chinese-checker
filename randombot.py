import random 

class RandomBot():
    def move(self, game):
        moves = game.potential_moves()
        return random.choice(moves)