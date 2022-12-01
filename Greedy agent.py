import random

class GreedyAgent():
    def move(self, pmoves):
        best_move = []
        length = 0
        for move in pmoves:
            if not best_move:
                best_move.append(move)
                length = abs(move.start_point.row - move.end_point.row)
            else:
                if abs(move.start_point.row - move.end_point.row) > length:
                    best_move.clean()
                    best_move.append(move)
                    length = abs(move.start_point.row - move.end_point.row)
                if abs(move.start_point.row - move.end_point.row) == length:
                    best_move.append(move)
                if abs(move.start_point.row - move.end_point.row) < length:
                    continue

        return random.choice(best_move)



