import random

class GreedyAgent():
    def move(self, game):
        best_move = []
        depth = 0
        for move in game.potential_moves():
            start_depth = move.start_point.row + move.start_point.col
            end_depth = move.end_point.row + move.end_point.col
            if abs(end_depth - start_depth) > depth:
                best_move.clear()
                best_move.append(move)
                depth = abs(end_depth-start_depth)
            if abs(end_depth-start_depth) == depth:
                best_move.append(move)
            if abs(end_depth-start_depth) < depth:
                continue

        return random.choice(best_move)



