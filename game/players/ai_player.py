import random
from game.players.player import Player


class BattleAI(Player):
    def __init__(self, name, x=0, y=0):
        super().__init__(name, x, y)
        self.reset()

    def reset(self):
        self.shot_history = set()
        self.hit_stack = []
        self.hunting_mode = False
        self.last_hit = None
        self.is_horizontal = None

    def perform_attack(self, opponent):
        if self.hunting_mode and self.hit_stack:
            row, col = self.hit_stack.pop()
        else:
            row, col = self.choose_attack_position()

        if opponent.board.is_coordinate_shot_at(row, col):
            self.perform_attack(opponent)
            return

        hit = opponent.board.register_shot(row, col)
        self.shot_history.add((row, col))

        if hit:
            print(f"AI hit at ({row}, {col})!")
            if opponent.board.is_ship_sunk_on(row, col):
                print(f"AI sunk a ship at ({row}, {col})!")
                self.reset()
            else:
                self.hunting_mode = True
                if self.last_hit:
                    self.determine_is_horizontal(row, col)
                    positions = self.generate_line_positions(row, col)
                else:
                    positions = self.generate_adjacent_positions(row, col)
                self.add_positions_to_stack(positions)
                self.last_hit = (row, col)
        else:
            print(f"AI missed at ({row}, {col})!")

    def choose_attack_position(self):
        while True:
            row = random.randint(0, self.board.rows_count - 1)
            col = random.randint(0, self.board.columns_count - 1)
            if (row, col) not in self.shot_history:
                return row, col

    def generate_adjacent_positions(self, row, col):
        return [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]

    def determine_is_horizontal(self, row, col):
        last_row, last_col = self.last_hit
        self.is_horizontal = row == last_row

    def generate_line_positions(self, row, col):
        if self.is_horizontal:
            return [(row, col - 1), (row, col + 1)]
        return [(row - 1, col), (row + 1, col)]

    def add_positions_to_stack(self, positions):
        valid_moves = [
            (new_row, new_col) for new_row, new_col in positions
            if (new_row, new_col) not in self.shot_history and
            self.board.is_coordinate_in_board(new_row, new_col)
        ]
        self.hit_stack.extend(valid_moves)
