import pygame
from pygame.sprite import Sprite

from game.visuals.utils.constants import RESOLUTION
from game.interface.base_board import BaseBoard
from game.visuals.visual_ship import Visual_Ship


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
        pygame.draw.rect(window, (168, 218, 220), tile_position)
        pygame.draw.rect(window, (69, 123, 157), tile_position, 1)

    def __repr__(self):
        return f"<Tile at {self.x}, {self.y}>"


class VisualBoard(Sprite, BaseBoard):

    def __init__(self, x=0, y=0):
        BaseBoard.__init__(self)
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.tiles = []
        self.populateWithTiles()

        self.initialize_visual_ships()
        self.random_shuffle_ships()

    def initialize_visual_ships(self):
        self.unplaced_ships = {Visual_Ship(
            ship.ship_length, self.get_tile_size()) for ship in self.unplaced_ships}

    def random_shuffle_ships(self):
        BaseBoard.random_shuffle_ships(self)
        self.update_ships_visual_position()

    def update_ships_visual_position(self):
        for (row, col), ship_list in self.ships_map.items():
            for ship in ship_list:
                new_x, new_y = self.getTileScreenPlacement(row, col)
                ship.update_visual_position(new_x, new_y)

    def draw_ships(self, window):
        for _, ship_list in self.ships_map.items():
            for ship in ship_list:
                ship.draw(window)

    def getTileScreenPlacement(self, row, col):
        return (self.x + col * VisualTile.TILE_SIZE, self.y + row * VisualTile.TILE_SIZE)

    def populateWithTiles(self):
        self.tiles = [[VisualTile(*self.getTileScreenPlacement(row, col))
                       for col in range(self.BOARD_COLS)] for row in range(self.BOARD_ROWS)]

    def draw_tiles(self, window):
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
        pos_x, pos_y = pos
        tile_size = self.get_tile_size()
        row = (pos_x - self.x) // tile_size
        col = (pos_y - self.y) // tile_size
        return row, col

    def draw(self, window):
        self.draw_tiles(window)
        self.draw_ships(window)

    def __repr__(self):
        return BaseBoard.__repr__(self)


b = VisualBoard(10, 10)
print(b.tiles)
