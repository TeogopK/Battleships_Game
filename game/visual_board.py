import pygame
from pygame.sprite import Sprite

from constants import RESOLUTION
from base_board import BaseBoard


class VisualTile(Sprite):
    TILE_SIZE = 60

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.size = self.TILE_SIZE * RESOLUTION

    def get_size(self):
        return self.size

    def drawTile(self, window):
        tile_position = (self.x,
                         self.y, self.size, self.size)
        pygame.draw.rect(window, (0, 0, 255), tile_position)
        pygame.draw.rect(window, (0, 100, 0), tile_position, 1)

    def __repr__(self):
        return f"<Tile at {self.x}, {self.y}>"


class VisualBoard(Sprite, BaseBoard):

    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.tiles = []
        self.populateWithTiles()

    def getTileScreenPlacement(self, row, col):
        return (self.x + col * VisualTile.TILE_SIZE, self.y + row * VisualTile.TILE_SIZE)

    def populateWithTiles(self):
        self.tiles = [[VisualTile(*self.getTileScreenPlacement(row, col))
                       for col in range(self.BOARD_COLS)] for row in range(self.BOARD_ROWS)]

    def drawTiles(self, window):
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                tile = self.tiles[row][col]
                tile.drawTile(window)

    def get_tile_size(self):
        return self.tiles[0][0].get_size()
    
    def get_right_border(self):
        return self.x + len(self.tiles) * self.get_tile_size()
    
    def get_bottom_border(self):
        return self.y + len(self.tiles) * self.get_tile_size()

    def is_position_in_board(self, pos):
        pos_x, pos_y = pos
        return self.x <= pos_x <= self.get_right_border() and self.y <= pos_y <= self.get_bottom_border()

    def get_row_col_by_mouse(self, pos):
        if not self.is_position_in_board(pos):
            raise ValueError(f"Invalid pos {pos}")

        pos_x, pos_y = pos
        tile_size = self.get_tile_size()
        row = (pos_x - self.x) // tile_size
        col = (pos_y - self.y) // tile_size
        return row, col

b = VisualBoard(10, 10)
print(b.tiles)
