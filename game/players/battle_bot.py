"""
Module for implementing a battle bot player in a Battleship game. The `BattleBot` class extends
the `Player` class to provide automated gameplay with a hunting strategy for attacking ships.
"""

import random
from game.players.player import Player


class BattleBot(Player):
    """
    A bot player that performs automated attacks in the Battleship game. The bot uses a hunting strategy
    to locate and sink ships, and handles attack logic based on the game state.
    """

    def __init__(self, network_client):
        """
        Initialize the BattleBot with a network client.

        Args:
            network_client: The network client used to communicate with the game server.
        """
        super().__init__("BattleBot", network_client)
        self.shot_history = None
        self.hit_stack = None
        self.hunting_mode = False
        self.last_hit = None
        self.is_horizontal = None

        self._reset_hunting_strategy()

    def _reset_hunting_strategy(self):
        """
        Reset the bot's hunting strategy, clearing shot history and hit stack.
        """
        self.shot_history = set()
        self.hit_stack = []
        self.hunting_mode = False
        self.last_hit = None
        self.is_horizontal = None

    def stop_bot(self):
        """
        Mark the bot as being in a finished battle.
        """
        self.is_in_finished_battle = True

    def perform_attack(self):
        """
        Perform an attack on the enemy board. The bot selects a position to attack and processes
        the result of the attack.
        """
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
        """
        Determine the position for the next attack based on the current strategy.

        Returns:
            tuple: (row, col) coordinates of the attack position.
        """
        if self.hunting_mode and self.hit_stack:
            return self.hit_stack.pop()
        return self._select_random_position()

    def _select_random_position(self):
        """
        Select a random position on the board that has not been attacked yet.

        Returns:
            tuple: (row, col) coordinates of the random position.
        """
        while True:
            row = random.randint(0, self.board.rows_count - 1)
            col = random.randint(0, self.board.columns_count - 1)
            if (row, col) not in self.shot_history:
                return row, col

    def _process_attack_result(self, response, row, col):
        """
        Process the result of an attack and update the bot's strategy based on whether a ship was hit or sunk.

        Args:
            response (dict): The response from the server containing the result of the attack.
            row (int): The row coordinate of the attack.
            col (int): The column coordinate of the attack.
        """
        has_hit_ship = response["args"]["has_hit_ship"]
        has_sunk_ship = response["args"]["has_sunk_ship"]

        if has_hit_ship:
            if has_sunk_ship:
                self._reset_hunting_strategy()
            else:
                self.hunting_mode = True
                self._update_hunting_strategy(row, col)

    def _update_hunting_strategy(self, row, col):
        """
        Update the bot's hunting strategy based on the latest hit.

        Args:
            row (int): The row coordinate of the last hit.
            col (int): The column coordinate of the last hit.
        """
        if self.last_hit:
            self._set_direction(row)
            positions = self._generate_line_positions(row, col)
        else:
            positions = BattleBot._generate_adjacent_positions(row, col)
        self._add_positions_to_stack(positions)
        self.last_hit = (row, col)

    @staticmethod
    def _generate_adjacent_positions(row, col):
        """
        Generate positions adjacent to the given coordinates.

        Args:
            row (int): The row coordinate.
            col (int): The column coordinate.

        Returns:
            list of tuples: List of adjacent positions.
        """
        return [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]

    def _set_direction(self, row):
        """
        Determine the direction of hunting based on the last hit.

        Args:
            row (int): The row coordinate of the last hit.
        """
        last_row, _ = self.last_hit
        self.is_horizontal = row == last_row

    def _generate_line_positions(self, row, col):
        """
        Generate positions in a line based on the direction of hunting.

        Args:
            row (int): The row coordinate of the last hit.
            col (int): The column coordinate of the last hit.

        Returns:
            list of tuples: List of line positions.
        """
        if self.is_horizontal:
            return [(row, col - 1), (row, col + 1)]
        return [(row - 1, col), (row + 1, col)]

    def _add_positions_to_stack(self, positions):
        """
        Add valid positions to the hit stack.

        Args:
            positions (list of tuples): List of positions to be added.
        """
        valid_moves = [
            (new_row, new_col)
            for new_row, new_col in positions
            if (new_row, new_col) not in self.shot_history and self.board.is_coordinate_in_board(new_row, new_col)
        ]
        self.hit_stack.extend(valid_moves)

    def start_main_loop(self):
        """
        Start the main loop for the bot, performing attacks as long as it's the bot's turn.
        """
        self.ask_to_receive_shot()

        while self.is_turn:
            self.perform_attack()
