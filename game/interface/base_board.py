"""Module for managing the board logic as an interface entity."""

import random
from collections import defaultdict
import json

from game.interface.ship import Ship


class BaseBoard:
    """Class for managing the board logic as an interface entity."""

    BOARD_ROWS_DEFAULT = BOARD_COLS_DEFAULT = 10

    def __init__(
        self,
        rows_count=BOARD_ROWS_DEFAULT,
        columns_count=BOARD_COLS_DEFAULT,
        unplaced_ships=None,
        ship_constructor=Ship,
    ):
        """
        Initializes a BaseBoard object.
        Args:
            rows_count (int, optional): The number of rows in the board. Defaults to BOARD_ROWS_DEFAULT.
            columns_count (int, optional): The number of columns in the board. Defaults to BOARD_COLS_DEFAULT.
            unplaced_ships (list, optional): A list of unplaced ships. Defaults to None.
            ship_constructor (class, optional): The ship constructor class. Defaults to Ship.
        """
        self.rows_count = rows_count
        self.columns_count = columns_count
        self.taken_coordinates = defaultdict(int)
        self.ships_map = defaultdict(list)
        self.unplaced_ships = (
            unplaced_ships if unplaced_ships is not None else BaseBoard._get_base_game_ships(ship_constructor)
        )

        self.shot_coordinates = defaultdict(int)
        self.all_hit_coordinates = set()

    @staticmethod
    def _get_base_game_ships(ship_constructor):
        """
        Returns a set of base game ships.

        Parameters:
        ship_constructor (function): A function that constructs a ship object.

        Returns:
        set: A set of base game ships.

        """
        return {
            ship_constructor(1),
            ship_constructor(1),
            ship_constructor(1),
            ship_constructor(1),
            ship_constructor(2),
            ship_constructor(2),
            ship_constructor(2),
            ship_constructor(3),
            ship_constructor(3),
            ship_constructor(4),
        }

    def _get_random_row_for_ship(self, ship_length, is_horizontal):
        """
        Returns a random row index for placing a ship on the game board.

        Parameters:
            ship_length (int): The length of the ship.
            is_horizontal (bool): Indicates whether the ship will be placed horizontally or vertically.

        Returns:
            int: A random row index within the valid range for placing the ship.
        """
        return random.randint(0, self.rows_count - (not is_horizontal) * ship_length)

    def _get_random_col_for_ship(self, ship_length, is_horizontal):
        """
        Generates a random column index for placing a ship on the game board.

        Parameters:
        - ship_length (int): The length of the ship.
        - is_horizontal (bool): Indicates whether the ship is placed horizontally or vertically.

        Returns:
        - int: The randomly generated column index.

        """
        return random.randint(0, self.columns_count - is_horizontal * ship_length)

    def random_shuffle_ships(self):
        """
        Randomly shuffles the placement of ships on the board.
        This method removes all existing ships from the board and then randomly places each ship
        in a valid position. The placement of each ship is determined by generating random row and
        column coordinates, as well as a random orientation (horizontal or vertical). The ship is
        then moved to the generated position and checked for validity. If the placement is valid,
        the ship is placed on the board, otherwise, a new random position is generated until a valid
        placement is found.
        """
        self._remove_all_ships()

        for ship in sorted(list(self.unplaced_ships), key=lambda ship: -ship.ship_length):
            placed = False

            while not placed:
                is_horizontal = random.choice([True, False])
                row = self._get_random_row_for_ship(ship.ship_length, is_horizontal)
                col = self._get_random_col_for_ship(ship.ship_length, is_horizontal)

                ship.move(row, col, is_horizontal)

                if self.is_ship_placement_valid(ship):
                    placed = True
                    self.place_ship(ship)

    def is_ship_placement_valid(self, ship):
        """
        Checks if the placement of a ship is valid on the board.

        Parameters:
            ship (Ship): The ship to be placed on the board.

        Returns:
            bool: True if the ship placement is valid, False otherwise.
        """
        return self._is_ship_in_board(ship) and not self._does_ship_overlap(ship)

    def _is_ship_in_board(self, ship):
        """
        Checks if all coordinates of a ship are within the board.

        Parameters:
            ship (Ship): The ship to check.

        Returns:
            bool: True if all coordinates of the ship are within the board, False otherwise.
        """
        return all(self.is_coordinate_in_board(row, col) for row, col in ship.coordinates)

    def place_ship(self, ship):
        """
        Places a ship on the board.

        Parameters:
            ship (Ship): The ship to be placed on the board.
        """
        self.ships_map[ship.row, ship.col].append(ship)
        self.unplaced_ships.discard(ship)
        self._occupy_coordinates_from_placement(ship)

    def remove_ship(self, ship):
        """
        Removes a ship from the board.

        Parameters:
            ship (Ship): The ship to be removed.
        """
        self.ships_map[ship.row, ship.col].remove(ship)
        self.unplaced_ships.add(ship)
        self._occupy_coordinates_from_placement(ship, True)

    def move_ship(self, ship, new_row, new_col, new_is_horizontal):
        """
        Moves a ship to a new position on the board.

        Parameters:
            ship (Ship): The ship to be moved.
            new_row (int): The new row position for the ship.
            new_col (int): The new column position for the ship.
            new_is_horizontal (bool): The new orientation of the ship.
        """
        old_row, old_col, old_is_horizontal = ship.row, ship.col, ship.is_horizontal
        self.remove_ship(ship)

        ship.move(new_row, new_col, new_is_horizontal)

        if not self.is_ship_placement_valid(ship):
            ship.move(old_row, old_col, old_is_horizontal)
            self.place_ship(ship)
            print("Can not move ship!")
            return

        self.place_ship(ship)

    def flip_ship(self, ship):
        """
        Flips the given ship horizontally or vertically.

        Parameters:
        - ship: The ship object to be flipped.
        """
        self.move_ship(ship, ship.row, ship.col, not ship.is_horizontal)

    def _get_adjacent_coordinates(self, ship):
        """
        Returns a list of adjacent coordinates to the given ship's coordinates.

        Parameters:
        - ship: The ship object for which to find adjacent coordinates.

        Returns:
        - adjacent_coords: A list of adjacent coordinates to the ship's coordinates.
        """
        adjacent_offsets = [(delta_x, delta_y) for delta_x in (-1, 0, 1) for delta_y in (-1, 0, 1)]

        adjacent_coords = set()
        for coord in ship.coordinates:
            for delta_x, delta_y in adjacent_offsets:
                adj_coord = (coord[0] + delta_x, coord[1] + delta_y)
                if self.is_coordinate_in_board(*adj_coord):
                    adjacent_coords.add(adj_coord)

        return adjacent_coords

    def _occupy_coordinates_from_placement(self, ship, reverse=False):
        """
        Occupies the coordinates adjacent to the given ship's placement.
        Args:
            ship (Ship): The ship object representing the ship being placed.
            reverse (bool, optional): Flag indicating whether to remove the coordinates
                from the occupied collection, doing the reverse. Defaults to False.
        """
        counter = 1 if not reverse else -1
        adjacent_coords = self._get_adjacent_coordinates(ship)

        for adj_coord in adjacent_coords:
            self.taken_coordinates[adj_coord] += counter

    def _does_ship_overlap(self, new_ship):
        """
        Checks if a new ship overlaps with any existing ships on the board.

        Parameters:
            new_ship (Ship): The new ship to be checked for overlap.

        Returns:
            bool: True if the new ship overlaps with any existing ships, False otherwise.
        """
        return any(self.taken_coordinates[coord] > 0 for coord in new_ship.coordinates)

    def _remove_all_ships(self):
        """
        Removes all ships from the board.

        This method iterates over all ship lists in the `ships_map` dictionary and removes each ship from the board
        by calling the `remove_ship` method.
        """
        for ship_list in self.ships_map.values():
            for ship in ship_list:
                self.remove_ship(ship)

    def get_ship_on_coord(self, row, col):
        """
        Returns the ship object located at the specified coordinates (row, col) on the board.

        Parameters:
        - row (int): The row index of the coordinate.
        - col (int): The column index of the coordinate.

        Returns:
        - ship (Ship): The ship object located at the specified coordinates.
        - None: If no ship is found at the specified coordinates.
        """
        for ship_list in self.ships_map.values():
            for ship in ship_list:
                if ship.is_coordinate_part_of_ship(row, col):
                    return ship

        return None

    def are_all_ships_sunk(self):
        """
        Check if all ships on the board are sunk.

        Returns:
            bool: True if all ships are sunk, False otherwise.
        """
        return all(not ship.is_alive for ship_list in self.ships_map.values() for ship in ship_list)

    def is_coordinate_in_board(self, row, col):
        """
        Checks if the given coordinate (row, col) is within the boundaries of the board.

        Parameters:
        - row (int): The row index of the coordinate.
        - col (int): The column index of the coordinate.

        Returns:
        - bool: True if the coordinate is within the board boundaries, False otherwise.
        """
        return 0 <= row < self.rows_count and 0 <= col < self.columns_count

    def is_coordinate_shot_at(self, row, col):
        """
        Check if a coordinate has been shot at.

        Parameters:
        - row (int): The row index of the coordinate.
        - col (int): The column index of the coordinate.

        Returns:
        - bool: True if the coordinate has been shot at, False otherwise.
        """
        return self.shot_coordinates[(row, col)] > 0

    def register_shot(self, row, col):
        """
        Registers a shot on the board at the specified coordinates.

        Args:
            row (int): The row index of the shot.
            col (int): The column index of the shot.

        Returns:
            Tuple[bool, bool, Optional[Ship]]: A tuple containing three values:
                - is_ship_hit (bool): True if a ship was hit, False otherwise.
                - is_ship_sunk (bool): True if a ship was sunk, False otherwise.
                - ship (Optional[Ship]): The ship object that was hit, or None if no ship was hit.
        """
        is_ship_hit = False
        is_ship_sunk = False
        self.shot_coordinates[(row, col)] += 1

        ship = self.get_ship_on_coord(row, col)
        if not ship:
            return is_ship_hit, is_ship_sunk, ship

        is_ship_hit = True
        ship.sunk_coordinate(row, col)
        self.all_hit_coordinates.update(ship.sunk_coordinates)

        is_ship_sunk = not ship.is_alive
        if is_ship_sunk:
            for adj_coordinate in self._get_adjacent_coordinates(ship):
                self.shot_coordinates[adj_coordinate] += 1

        return is_ship_hit, is_ship_sunk, ship

    def __repr__(self):
        """
        Returns a string representation of the BaseBoard object.
        The string representation includes the ships on the board, marked as their lengths,
        and the taken coordinates marked as "+".

        Returns:
            str: A string representation of the BaseBoard object.
        """
        repr_str = ""
        for ship in self.ships_map.values():
            repr_str += str(ship) + "\n"

        board_representation = [["-" for _ in range(10)] for _ in range(10)]

        for (row, col), value in self.taken_coordinates.items():
            if value:
                board_representation[row][col] = "+"

        for ship_list in self.ships_map.values():
            for ship in ship_list:
                for row, col in ship.coordinates:
                    board_representation[row][col] = str(ship.ship_length)

        for row in board_representation:
            repr_str += " ".join(row) + "\n"

        return repr_str

    def serialize_board(self):
        """
        Serializes the board data into a JSON string.
        Returns:
            str: The serialized board data in JSON format.
        """
        ships_data = []
        for ship_list in self.ships_map.values():
            for ship in ship_list:
                ships_data.append(ship.serialize())

        board_data = {
            "rows_count": self.rows_count,
            "columns_count": self.columns_count,
            "ships": ships_data,
        }
        return json.dumps(board_data)

    def place_ships_from_json(self, board_json):
        """
        Places ships on the board based on the provided JSON data.

        Args:
            board_json (dict): The JSON data containing information about the ships.

        Raises:
            ValueError: If an invalid ship placement is detected.
        """
        for ship_json in board_json["ships"]:
            ship = Ship.deserialize(ship_json)
            if self.is_ship_placement_valid(ship):
                self.place_ship(ship)
            else:
                raise ValueError("Invalid ship placement detected.")

    @staticmethod
    def deserialize_board(board_data):
        """
        Deserialize the board data and create a BaseBoard object.

        Args:
            board_data (str): The serialized board data.

        Returns:
            BaseBoard: The deserialized BaseBoard object.
        """
        board_json = json.loads(board_data)

        board = BaseBoard(
            rows_count=board_json["rows_count"],
            columns_count=board_json["columns_count"],
        )

        board.place_ships_from_json(board_json)

        return board


class BaseBoardEnemyView(BaseBoard):
    """Class that represents the enemy view of the board without knowing where each ship is."""

    def __init__(
        self,
        rows_count=BaseBoard.BOARD_ROWS_DEFAULT,
        columns_count=BaseBoard.BOARD_COLS_DEFAULT,
    ):
        """
        Initializes a BaseBoard object.

        Args:
            rows_count (int): The number of rows in the board. Defaults to BaseBoard.BOARD_ROWS_DEFAULT.
            columns_count (int): The number of columns in the board. Defaults to BaseBoard.BOARD_COLS_DEFAULT.
        """
        super().__init__(rows_count, columns_count, set())

    def register_shot_on_view(self, row, col, is_hit):
        """
        Registers a shot on the view board.

        Args:
            row (int): The row index of the shot.
            col (int): The column index of the shot.
            is_hit (bool): Indicates whether the shot is a hit or a miss.
        """

        self.shot_coordinates[(row, col)] += 1

        if is_hit:
            self.all_hit_coordinates.add((row, col))

    def reveal_ship(self, ship, reveal_adjacent=False):
        """
        Reveals a ship on the board and optionally reveals adjacent coordinates.

        Args:
            ship: The ship object to be revealed on the board.
            reveal_adjacent (bool): Flag indicating whether to reveal adjacent coordinates.

        Returns:
            bool: True if the ship was successfully revealed, False otherwise.
        """
        if not self.is_ship_placement_valid(ship):
            return False

        self.place_ship(ship)

        if reveal_adjacent:
            for adj_coordinate in self._get_adjacent_coordinates(ship):
                self.shot_coordinates[adj_coordinate] += 1

        return True

    def reveal_ships_from_board_data(self, board_data):
        """
        Reveal ships on the board based on the provided board data.

        Parameters:
        - board_data (str): The serialized board data containing ship information.
        """
        board_json = json.loads(board_data)

        for ship_json in board_json["ships"]:
            ship = Ship.deserialize(ship_json)
            self.reveal_ship(ship)
