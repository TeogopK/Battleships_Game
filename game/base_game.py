import random
import pygame

from board import Board
from ship import Ship


class BaseGame():

    def __init__(self):
        self.board = Board()
        self.taken_coordinates = set()
        self.ships = [
            Ship(1),
            Ship(1),
            Ship(1),
            Ship(1),
            Ship(2),
            Ship(2),
            Ship(2),
            Ship(3),
            Ship(3),
            Ship(4)
        ]

    def get_random_start_for_ship(self, ship_length, is_horizontal, board_border):
        return random.randint(0, board_border - 1 - is_horizontal * ship_length)

    def random_shuffle_ships(self):
        for ship in self.ships:
            placed = False

            while not placed:
                is_horizontal = random.choice([True, False])
                row = self.get_random_start_for_ship(
                    ship.ship_length, is_horizontal, self.board.BOARD_ROWS)
                col = self.get_random_start_for_ship(
                    ship.ship_length, is_horizontal, self.board.BOARD_COLS)

                ship.move_ship(row, col, is_horizontal)

                if ship.is_in_board(self.board) and not self.check_overlap(ship):
                    placed = True
                    self.take_coordinates_from_placement(ship)

    def take_coordinates_from_placement(self, ship):
        adjacent_offsets = [
            (dx, dy)
            for dx in (-1, 0, 1) # Change to 0 only to allow adjacency
            for dy in (-1, 0, 1)
        ]

        for coord in ship.coordinates:
            for dx, dy in adjacent_offsets:
                adj_coord = (coord[0] + dx, coord[1] + dy)
                self.taken_coordinates.add(adj_coord)

    def check_overlap(self, new_ship):
        return any(coord in self.taken_coordinates for coord in new_ship.coordinates)

    def __repr__(self):

        repr_str = ""
        for ship in self.ships:
            repr_str += str(ship) + '\n'

        board_representation = [['-' for _ in range(10)] for _ in range(10)]

        for ship in self.ships:
            for row, col in ship.coordinates:
                board_representation[row][col] = str(ship.ship_length)

        for row in board_representation:
            repr_str += ' '.join(row) + '\n'

        return repr_str


# Example usage:
if __name__ == "__main__":
    game = BaseGame()
    game.random_shuffle_ships()
    print(game)
