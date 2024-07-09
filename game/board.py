import pygame
from pygame.sprite import Sprite

from constants import TILE_SIZE, BOARD_ROWS, BOARD_COLS


class Tile(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.size = TILE_SIZE
        self.shot_count = 0

    def increaseShotCount(self):
        self.shot_count += 1

    def drawTile(self, window):
        tile_position = (self.x,
                                 self.y, self.size, self.size)
        pygame.draw.rect(window, (0, 0, 255), tile_position)
        pygame.draw.rect(window, (0, 0, 0), tile_position, 1)



    def __repr__(self):
        return f"<Tile at {self.x}, {self.y}>"


class Board(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.tiles = []
        self.populateWithTiles()

    def populateWithTiles(self):
        self.tiles = [[Tile(self.x + col * TILE_SIZE, self.y + row * TILE_SIZE)
                       for col in range(BOARD_COLS)] for row in range(BOARD_ROWS)]

    def drawBoard(self, window):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                tile = self.tiles[row][col]
                tile.drawTile(window)

b = Board(10, 10)
print(b.tiles)
