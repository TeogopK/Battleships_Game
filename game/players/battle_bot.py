import random
from game.players.player import Player


class BattleBot(Player):
    def __init__(
        self,
        network_client,
    ):
        super().__init__("BattleBot", network_client)
        self._reset_hunting_strategy()

    def _reset_hunting_strategy(self):
        self.shot_history = set()
        self.hit_stack = []
        self.hunting_mode = False
        self.last_hit = None
        self.is_horizontal = None

    def stop_bot(self):
        self.is_in_finished_battle = True

    def perform_attack(self):
        if self.is_in_finished_battle:
            self.is_turn = False
            return

        row, col = self._get_attack_position()

        if self.enemy_board_view.is_coordinate_shot_at(row, col):
            self.perform_attack()
            return

        response = self.shot(row, col)
        if response["status"] == "error":
            self.perform_attack()
            return

        self._process_attack_result(response, row, col)

    def _get_attack_position(self):
        if self.hunting_mode and self.hit_stack:
            return self.hit_stack.pop()
        return self._select_random_position()

    def _select_random_position(self):
        while True:
            row = random.randint(0, self.board.rows_count - 1)
            col = random.randint(0, self.board.columns_count - 1)
            if (row, col) not in self.shot_history:
                return row, col

    def _process_attack_result(self, response, row, col):
        has_hit_ship = response["args"]["has_hit_ship"]
        has_sunk_ship = response["args"]["has_sunk_ship"]

        if has_hit_ship:
            if has_sunk_ship:
                self._reset_hunting_strategy()
            else:
                self.hunting_mode = True
                self._update_hunting_strategy(row, col)

    def _update_hunting_strategy(self, row, col):
        if self.last_hit:
            self._set_direction(row, col)
            positions = self._generate_line_positions(row, col)
        else:
            positions = self._generate_adjacent_positions(row, col)
        self._add_positions_to_stack(positions)
        self.last_hit = (row, col)

    def _generate_adjacent_positions(self, row, col):
        return [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]

    def _set_direction(self, row, col):
        last_row, last_col = self.last_hit
        self.is_horizontal = row == last_row

    def _generate_line_positions(self, row, col):
        if self.is_horizontal:
            return [(row, col - 1), (row, col + 1)]
        return [(row - 1, col), (row + 1, col)]

    def _add_positions_to_stack(self, positions):
        valid_moves = [
            (new_row, new_col)
            for new_row, new_col in positions
            if (new_row, new_col) not in self.shot_history
            and self.board.is_coordinate_in_board(new_row, new_col)
        ]
        self.hit_stack.extend(valid_moves)

    def start_main_loop(self):
        self.ask_to_receive_shot()

        while self.is_turn:
            self.perform_attack()
