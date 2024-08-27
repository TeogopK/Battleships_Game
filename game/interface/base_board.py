import random
from collections import defaultdict
import json

from game.interface.ship import Ship


class BaseBoard:
    BOARD_ROWS_DEFAULT = BOARD_COLS_DEFAULT = 10

    def __init__(
        self,
        rows_count=BOARD_ROWS_DEFAULT,
        columns_count=BOARD_COLS_DEFAULT,
        unplaced_ships=None,
        ship_constructor=Ship,
    ):
        self.rows_count = rows_count
        self.columns_count = columns_count
        self.taken_coordinates = defaultdict(int)
        self.ships_map = defaultdict(list)
        self.unplaced_ships = (
            unplaced_ships
            if unplaced_ships != None
            else BaseBoard.get_base_game_ships(ship_constructor)
        )

        self.shot_coordinates = defaultdict(int)
        self.all_hit_coordinates = set()

    @staticmethod
    def get_base_game_ships(ship_constructor):
        return {
            # ship_constructor(1),
            # ship_constructor(1),
            # ship_constructor(1),
            # ship_constructor(1),
            # ship_constructor(2),
            # ship_constructor(2),
            # ship_constructor(2),
            # ship_constructor(3),
            # ship_constructor(3),
            ship_constructor(9),
        }

    def get_random_start_for_ship(self, ship_length, is_horizontal, board_border):
        return random.randint(0, board_border - 1 - is_horizontal * ship_length)

    def random_shuffle_ships(self):
        self.remove_all_ships()

        for ship in sorted(
            list(self.unplaced_ships), key=lambda ship: -ship.ship_length
        ):
            placed = False

            while not placed:
                is_horizontal = random.choice([True, False])
                row = self.get_random_start_for_ship(
                    ship.ship_length, is_horizontal, self.rows_count
                )
                col = self.get_random_start_for_ship(
                    ship.ship_length, is_horizontal, self.columns_count
                )

                ship.move(row, col, is_horizontal)

                if self.is_ship_placement_valid(ship):
                    placed = True
                    self.place_ship(ship)

    def is_ship_placement_valid(self, ship):
        return self.is_ship_in_board(ship) and not self.does_ship_overlap(ship)

    def is_ship_in_board(self, ship):
        return all(
            self.is_coordinate_in_board(row, col) for row, col in ship.coordinates
        )

    def place_ship(self, ship):
        self.ships_map[ship.row, ship.col].append(ship)
        self.unplaced_ships.discard(ship)
        self.occupy_coordinates_from_placement(ship)

    def remove_ship(self, ship):
        self.ships_map[ship.row, ship.col].remove(ship)
        self.unplaced_ships.add(ship)
        self.occupy_coordinates_from_placement(ship, True)

    def move_ship(self, ship, new_row, new_col, new_is_horizontal):
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
        self.move_ship(ship, ship.row, ship.col, not ship.is_horizontal)

    def is_coordinate_in_board(self, row, col):
        return 0 <= row < self.rows_count and 0 <= col < self.columns_count

    def get_adjacent_coordinates(self, ship):
        """Get all adjacent coordinates around a ship's position."""
        adjacent_offsets = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]

        adjacent_coords = []
        for coord in ship.coordinates:
            for dx, dy in adjacent_offsets:
                adj_coord = (coord[0] + dx, coord[1] + dy)
                if self.is_coordinate_in_board(*adj_coord):
                    adjacent_coords.append(adj_coord)

        return adjacent_coords

    def occupy_coordinates_from_placement(self, ship, reverse=False):
        """Mark or unmark coordinates as occupied based on ship placement."""
        counter = 1 if not reverse else -1
        adjacent_coords = self.get_adjacent_coordinates(ship)

        for adj_coord in adjacent_coords:
            self.taken_coordinates[adj_coord] += counter

    def does_ship_overlap(self, new_ship):
        return any(self.taken_coordinates[coord] > 0 for coord in new_ship.coordinates)

    def remove_all_ships(self):
        for ship_list in self.ships_map.values():
            for ship in ship_list:
                self.remove_ship(ship)

    def is_there_a_ship_on_coord(self, row, col):
        for ship_list in self.ships_map.values():
            for ship in ship_list:
                if ship.is_coordinate_part_of_ship(row, col):
                    return True

        return False

    def get_ship_on_coord(self, row, col):
        for ship_list in self.ships_map.values():
            for ship in ship_list:
                if ship.is_coordinate_part_of_ship(row, col):
                    return ship

        return None

    def is_ship_sunk_on(self, row, col):
        return not self.get_ship_on_coord(row, col).is_alive

    def are_all_ships_sunk(self):
        return all(
            not ship.is_alive
            for ship_list in self.ships_map.values()
            for ship in ship_list
        )

    def is_coordinate_in_board(self, row, col):
        return 0 <= row < self.rows_count and 0 <= col < self.columns_count

    def is_coordinate_shot_at(self, row, col):
        return self.shot_coordinates[(row, col)] > 0

    def register_shot(self, row, col):
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
            for adj_coordinate in self.get_adjacent_coordinates(ship):
                self.shot_coordinates[adj_coordinate] += 1

        return is_ship_hit, is_ship_sunk, ship

    def __repr__(self):
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

    def _place_ships_from_json(self, board_json):
        for ship_json in board_json["ships"]:
            ship = Ship.deserialize(ship_json)
            if self.is_ship_placement_valid(ship):
                self.place_ship(ship)
            else:
                raise ValueError("Invalid ship placement detected.")

    @staticmethod
    def deserialize_board(board_data):
        board_json = json.loads(board_data)

        board = BaseBoard(
            rows_count=board_json["rows_count"],
            columns_count=board_json["columns_count"],
        )

        board._place_ships_from_json(board_json)

        return board


class BaseBoardEnemyView(BaseBoard):
    def __init__(
        self,
        rows_count=BaseBoard.BOARD_ROWS_DEFAULT,
        columns_count=BaseBoard.BOARD_COLS_DEFAULT,
    ):
        super().__init__(rows_count, columns_count, set())

    def register_shot(self, row, col, is_hit):
        self.shot_coordinates[(row, col)] += 1

        if is_hit:
            self.all_hit_coordinates.add((row, col))

    def reveal_ship(self, ship, reveal_adjacent=False):
        if not self.is_ship_placement_valid(ship):
            return

        self.place_ship(ship)

        if reveal_adjacent:
            for adj_coordinate in self.get_adjacent_coordinates(ship):
                self.shot_coordinates[adj_coordinate] += 1

        return True

    def reveal_ships_from_board_data(self, board_data):
        board_json = json.loads(board_data)

        for ship_data in board_json["ships"]:
            ship = Ship.deserialize(ship_data)
            self.reveal_ship(ship)
