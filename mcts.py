import random
import math
from randombot import RandomBot
from player import Player

def cal_score(game_state, player):
    score = 0
    bias_fine = 0.2
    last_chess_fine = 0.5
    last_chess = 0 
    for p in game_state.board.get_all_pieces(player.value):
        if player == Player.red:
            layer = p.row + p.col #what layer is p in
            if last_chess < 10 - layer:
                last_chess = 10 - layer
            score += layer - bias_fine * abs(p.row - p.col)
        else:
            layer = p.row + p.col
            last_chess = max(last_chess, layer)
            score += (10-layer) - bias_fine * abs(p.row - p.col)
    score += 60 + bias_fine * 7 - last_chess_fine * last_chess
    return score 

class MCTSNode():
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.win_counts = {
            Player.red: 0,
            Player.blue: 0,
        }
        self.num = 0
        self.children = []
        self.potential_moves = game_state.potential_moves()
    
    def add_random_child(self):
        p = random.randint(0, len(self.potential_moves) - 1)
        new_move = self.potential_moves.pop(p)
        new_game_state = self.game_state.apply_move(new_move)
        new_node = MCTSNode(new_game_state, self, new_move)
        self.children.append(new_node)
        return new_node
    
    def record_win(self, winner):
        if winner is not None:
            self.win_counts[winner] += 1
        self.num += 1
    
    def check_child(self):
        return len(self.potential_moves) > 0

    def is_over(self):
        return self.game_state.is_over()

    def winning_rate(self, player):
        return float(self.win_counts[player]) / float(self.num)

class MCTSAgent():
    def __init__(self, num_games, temperature):
        self.num_games = num_games
        self.temperature = temperature


    def move(self, game_state):
        root = MCTSNode(game_state)

        for i in range(self.num_games):
            node = root
            #choose best available child
            while (not node.check_child()) and (not node.is_over()):
                node = self.select_child(node)

            if node.check_child():
                node = node.add_random_child()

            winner = self.simulate_random_game(node.game_state)
            
            while node is not None:
                node.record_win(winner)
                node = node.parent

        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_rate(game_state.next_player)
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        return best_move

    def select_child(self, node):
        total_rollouts = sum(child.num for child in node.children)
        log_rollouts = math.log(total_rollouts)

        best_score = -1
        best_child = None
        
        #calculate UCB 
        for child in node.children:
            win_percentage = child.winning_rate(node.game_state.next_player)
            exploration_factor = math.sqrt(log_rollouts / child.num)
            uct_score = win_percentage + self.temperature * exploration_factor
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child


    @staticmethod
    def simulate_random_game(game):
        bots = {
            Player.red: RandomBot(),
            Player.blue: RandomBot(),
        }
        rounds = 0
        while not game.is_over() and rounds < 400:
            bot_move = bots[game.next_player].move(game)
            game = game.apply_move(bot_move)
            rounds += 1
        if rounds == 400:
            red_score = cal_score(game, Player.red)
            blue_score = cal_score(game, Player.blue)
            return Player.red if red_score > blue_score else Player.blue 
        return game.winner()