import pygame
from pygame.sprite import Sprite

from game.visuals.utils.constants import RESOLUTION
from game.interface.base_board import BaseBoard, BaseBoardEnemyView
from game.visuals.visual_ship import Visual_Ship

import game.visuals.utils.colors as colors
from game.visuals.utils.shapes import DrawUtils


class VisualTile(Sprite):
    TILE_SIZE = 50

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.size = self.TILE_SIZE * RESOLUTION

    def get_size(self):
        return self.size

    def draw_tile(self, window):
        tile_position = (self.x, self.y, self.size, self.size)
        pygame.draw.rect(window, colors.TILE_MAIN_COLOR, tile_position)
        pygame.draw.rect(window, colors.TILE_BORDER_COLOR, tile_position, 1)

    def __repr__(self):
        return f"<Tile at {self.x}, {self.y}>"


class VisualBoard(Sprite, BaseBoard):
    def __init__(self, x=0, y=0):
        BaseBoard.__init__(self)
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.tiles = []
        self.populate_with_tiles()

        self.initialize_visual_ships()
        self.random_shuffle_ships()

    def initialize_visual_ships(self):
        self.unplaced_ships = {
            Visual_Ship(ship.ship_length, coordinate_size=self.get_tile_size())
            for ship in self.unplaced_ships
        }

    def random_shuffle_ships(self):
        BaseBoard.random_shuffle_ships(self)
        self.update_ships_visual_position()

    def update_ships_visual_position(self):
        for (row, col), ship_list in self.ships_map.items():
            for ship in ship_list:
                new_x, new_y = self.get_tile_screen_placement(row, col)
                ship.update_visual_position(new_x, new_y)

    def update_individual_ship_visual_position(self, ship):
        new_x, new_y = self.get_tile_screen_placement(ship.row, ship.col)
        ship.update_visual_position(new_x, new_y)

    def draw_ships(self, window):
        for ship_list in self.ships_map.values():
            for ship in ship_list:
                ship.draw(window)

        for ship in self.unplaced_ships:
            ship.draw(window)

    def get_tile_screen_placement(self, row, col):
        return (
            self.x + col * VisualTile.TILE_SIZE,
            self.y + row * VisualTile.TILE_SIZE,
        )

    def populate_with_tiles(self):
        self.tiles = [
            [
                VisualTile(*self.get_tile_screen_placement(row, col))
                for col in range(self.columns_count)
            ]
            for row in range(self.rows_count)
        ]

    def draw_tiles(self, window):
        for row in range(self.rows_count):
            for col in range(self.columns_count):
                tile = self.tiles[row][col]
                tile.draw_tile(window)

    def get_tile_size(self):
        return self.tiles[0][0].get_size()

    def get_right_border(self):
        return self.x + len(self.tiles) * self.get_tile_size()

    def get_bottom_border(self):
        return self.y + len(self.tiles) * self.get_tile_size()

    def is_position_in_board(self, pos):
        pos_x, pos_y = pos
        return (
            self.x <= pos_x <= self.get_right_border()
            and self.y <= pos_y <= self.get_bottom_border()
        )

    def get_row_col_by_mouse(self, pos):
        pos_x, pos_y = pos
        tile_size = self.get_tile_size()
        row = (pos_y - self.y) // tile_size
        col = (pos_x - self.x) // tile_size
        return row, col

    def draw_sunk_ships(self, window):
        for ship_list in self.ships_map.values():
            for ship in ship_list:
                if not ship.is_alive:
                    ship.set_color(colors.SHIP_SUNK_COLOR)
                    ship.draw(window)

    def draw_hits(self, window):
        for row, col in self.all_hit_coordinates:
            tile = self.tiles[row][col]
            hit_position = (tile.x, tile.y, tile.size, tile.size)
            DrawUtils.draw_cross(
                window, tile.x, tile.y, tile.size, colors.SHOT_HIT_COLOR
            )

    def draw_misses(self, window):
        for (row, col), hit_count in self.shot_coordinates.items():
            if hit_count > 0 and (row, col) not in self.all_hit_coordinates:
                tile = self.tiles[row][col]
                miss_position = (tile.x, tile.y, tile.size, tile.size)
                DrawUtils.draw_circle(
                    window, tile.x, tile.y, tile.size, colors.SHOT_MISS_COLOR
                )

    def draw_board_border(self, window):
        BORDER_WIDTH = 5
        border_rect = pygame.Rect(
            self.x - BORDER_WIDTH,
            self.y - BORDER_WIDTH,
            self.get_right_border() - self.x + BORDER_WIDTH * 2,
            self.get_bottom_border() - self.y + BORDER_WIDTH * 2,
        )
        pygame.draw.rect(window, colors.BOARD_BORDER_COLOR, border_rect, BORDER_WIDTH)

    def draw(self, window):
        self.draw_board_border(window)
        self.draw_tiles(window)
        self.draw_ships(window)
        self.draw_hits(window)
        self.draw_sunk_ships(window)
        self.draw_misses(window)

    def move_ship(self, ship, new_row, new_col, new_is_horizontal):
        BaseBoard.move_ship(self, ship, new_row, new_col, new_is_horizontal)
        self.update_individual_ship_visual_position(ship)

    def place_ship(self, ship):
        BaseBoard.place_ship(self, ship)
        self.update_individual_ship_visual_position(ship)

    def __repr__(self):
        return BaseBoard.__repr__(self)


class VisualBoardEnemyView(VisualBoard, BaseBoardEnemyView):
    def __init__(self, x=0, y=0):
        VisualBoard.__init__(self, x, y)
        BaseBoardEnemyView.__init__(self)

    def reveal_sunk_ship(self, ship):
        visual_ship = Visual_Ship(
            ship.ship_length,
            ship.row,
            ship.col,
            ship.is_horizontal,
            ship.is_alive,
            ship.sunk_coordinates,
            coordinate_size=self.get_tile_size(),
        )
        BaseBoardEnemyView.reveal_sunk_ship(self, visual_ship)
