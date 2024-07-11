import random
import pygame

from board import Board
from ship import Ship


class BaseGame():

    def __init__(self):
        self.board = Board()
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

    def check_overlap(self, new_ship):
        for ship in self.ships:
            if ship == new_ship:
                continue
            if any(coord in ship.coordinates for coord in new_ship.coordinates):
                return True
        return False

    def __repr__(self):

        repr_str = ""
        for ship in self.ships:
            repr_str += str(ship) + '\n'

        board_representation = [['-' for _ in range(10)] for _ in range(10)]

        for ship in self.ships:
            for row, col in ship.coordinates:
                board_representation[row][col] = 'x'

        for row in board_representation:
            repr_str += ' '.join(row) + '\n'

        return repr_str


# Example usage:
if __name__ == "__main__":
    game = BaseGame()
    game.random_shuffle_ships()
    print(game)
