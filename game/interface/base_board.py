import random
from collections import defaultdict

from game.interface.ship import Ship


class BaseBoard():
    BOARD_ROWS = BOARD_COLS = 10

    def __init__(self, rows_count=10, columns_count=10):
        self.rows_count = rows_count
        self.columns_count = columns_count
        self.taken_coordinates = set()
        self.ships_map = defaultdict(list)
        self.unplaced_ships = self.get_base_game_ships()

    def get_base_game_ships(self):
        return {Ship(1),
                Ship(1),
                Ship(1),
                Ship(1),
                Ship(2),
                Ship(2),
                Ship(2),
                Ship(3),
                Ship(3),
                Ship(4)
                }

    def get_random_start_for_ship(self, ship_length, is_horizontal, board_border):
        return random.randint(0, board_border - 1 - is_horizontal * ship_length)

    def random_shuffle_ships(self):
        for ship in sorted(list(self.unplaced_ships), key=lambda ship: -ship.ship_length):
            placed = False

            while not placed:
                is_horizontal = random.choice([True, False])
                row = self.get_random_start_for_ship(
                    ship.ship_length, is_horizontal, self.rows_count)
                col = self.get_random_start_for_ship(
                    ship.ship_length, is_horizontal, self.columns_count)

                ship.move(row, col, is_horizontal)

                if self.is_ship_placement_valid(ship):
                    placed = True
                    self.place_ship(ship)

    def is_ship_placement_valid(self, ship):
        return self.is_ship_in_board(ship) and not self.check_overlap(ship)

    def is_ship_in_board(self, ship):
        return all(0 <= row < self.rows_count and 0 <= col < self.columns_count for row, col in ship.coordinates)

    def place_ship(self, ship):
        self.ships_map[ship.row, ship.col].append(ship)
        self.unplaced_ships.add(ship)
        self.occupy_coordinates_from_placement(ship)

    def remove_ship(self, ship):
        self.ships_map[ship.row, ship.col].remove(ship)
        self.unplaced_ships.remove(ship)
        self.occupy_coordinates_from_placement(ship, True)

    def move_ship(self, ship, new_row, new_col, new_is_horizontal):
        old_row, old_col, old_is_horizontal = ship.row, ship.col, ship.is_horizontal
        self.remove_ship(ship)

        ship.move(new_row, new_col, new_is_horizontal)

        if not self.is_ship_placement_valid(ship):
            ship.move(old_row, old_col, old_is_horizontal)
            self.place_ship(ship)
            raise ValueError("Can not move ship")

        self.place_ship(ship)

    def flip_ship(self, ship):
        self.move_ship(ship, ship.row, ship.col, not ship.is_horizontal)

    def occupy_coordinates_from_placement(self, ship, reverse=False):
        adjacent_offsets = [
            (dx, dy)
            for dx in (-1, 0, 1)  # Change to 0 only to allow adjacency
            for dy in (-1, 0, 1)
        ]

        function_string = 'add' if not reverse else 'discard'
        function = self.taken_coordinates.__getattribute__(function_string)

        for coord in ship.coordinates:
            for dx, dy in adjacent_offsets:
                adj_coord = (coord[0] + dx, coord[1] + dy)
                function(adj_coord)

    def check_overlap(self, new_ship):
        return any(coord in self.taken_coordinates for coord in new_ship.coordinates)

    def remove_all_ships(self):
        self.taken_coordinates = set()
        self.ships_map = defaultdict(list)
        self.unplaced_ships = self.get_base_game_ships()

    def __repr__(self):

        repr_str = ""
        for ship in self.ships_map.values():
            repr_str += str(ship) + '\n'

        board_representation = [['-' for _ in range(10)] for _ in range(10)]

        for ship_list in self.ships_map.values():
            for ship in ship_list:
                for row, col in ship.coordinates:
                    board_representation[row][col] = str(ship.ship_length)

        for row in board_representation:
            repr_str += ' '.join(row) + '\n'

        return repr_str


# Example usage:
if __name__ == "__main__":
    game = BaseBoard()
    game.random_shuffle_ships()
    print(game)

    for ship in list(game.ships_map.values())[0]:
        print("Flipping ship", ship)
        game.flip_ship(ship)
        print(game)
        break
