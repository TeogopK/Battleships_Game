from board import Board
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ship_length, row=None, col=None, is_horizontal=True):
        super().__init__()
        self.ship_length = ship_length
        self.move(row, col, is_horizontal)

    def fill_coordinates(self):
        if self.row == None and self.col == None:
            self.coordinates = []
            return

        self.coordinates = [(self.row + tile * (not self.is_horizontal), self.col + tile *
                             self.is_horizontal) for tile in range(self.ship_length)]

    def is_in_board(self, board):
        return all(0 <= row < board.BOARD_ROWS and 0 <= col < board.BOARD_COLS for row, col in self.coordinates)

    def flip(self):
        self.is_horizontal = not self.is_horizontal
        self.fill_coordinates()

    def move(self, row, col, is_horizontal):
        self.row = row
        self.col = col
        self.is_horizontal = is_horizontal
        self.fill_coordinates()

    def draw_ship(self, board):
        pass

    def __repr__(self):
        return f"<Ship with length {self.ship_length}, {self.is_horizontal} at {self.coordinates}>"


s = Ship(5, 10, 1, False)
s.fill_coordinates()
print(s.is_in_board(Board(1, 1)))
print(s)
