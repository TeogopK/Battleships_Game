import pygame
from pygame.sprite import Sprite

from constants import RESOLUTION


class Tile(Sprite):
    TILE_SIZE = 60

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.size = self.TILE_SIZE * RESOLUTION
        self.shot_count = 0

    def increaseShotCount(self):
        self.shot_count += 1

    def drawTile(self, window):
        tile_position = (self.x,
                         self.y, self.size, self.size)
        pygame.draw.rect(window, (0, 0, 255), tile_position)
        pygame.draw.rect(window, (0, 100, 0), tile_position, 1)

    def __repr__(self):
        return f"<Tile at {self.x}, {self.y}>"


class Board(Sprite):
    BOARD_ROWS = BOARD_COLS = 10 * RESOLUTION

    def __init__(self, x = 0, y = 0):
        super().__init__()
        self.x = x
        self.y = y
        self.tiles = []
        self.populateWithTiles()

    def getTileScreenPlacement(self, row, col):
        return (self.x + col * Tile.TILE_SIZE, self.y + row * Tile.TILE_SIZE)

    def populateWithTiles(self):
        self.tiles = [[Tile(*self.getTileScreenPlacement(row, col))
                       for col in range(self.BOARD_COLS)] for row in range(self.BOARD_ROWS)]

    def drawBoard(self, window):
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                tile = self.tiles[row][col]
                tile.drawTile(window)



b = Board(10, 10)
print(b.tiles)
