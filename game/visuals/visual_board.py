import pygame
from pygame.sprite import Sprite

from game.visuals.utils.constants import RESOLUTION
from game.interface.base_board import BaseBoard, BaseBoardEnemyView
from game.visuals.visual_ship import VisualShip

from game.visuals.utils import colors
from game.visuals.utils.draw_utils import DrawUtils


class VisualTile(Sprite):
    TILE_SIZE = 50

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.size = self.TILE_SIZE * RESOLUTION
        self.is_hovered = False

    def get_size(self):
        return self.size

    def draw_tile(self, window):
        tile_position = (self.x, self.y, self.size, self.size)
        tile_color = colors.TILE_HOVER_COLOR if self.is_hovered else colors.TILE_MAIN_COLOR
        pygame.draw.rect(window, tile_color, tile_position)
        pygame.draw.rect(window, colors.TILE_BORDER_COLOR, tile_position, 1)

    def set_hover(self, is_hovered):
        self.is_hovered = is_hovered

    def __repr__(self):
        return f"<Tile at {self.x}, {self.y}>"


class VisualBoard(Sprite, BaseBoard):
    BORDER_WIDTH = 5

    def __init__(self, x=0, y=0):
        BaseBoard.__init__(self, ship_constructor=VisualShip)
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.tiles = []
        self._populate_with_tiles()

        self._initialize_visual_ships()
        self.random_shuffle_ships()

    def _initialize_visual_ships(self):
        for ship in self.unplaced_ships:
            ship.coordinate_size = self.get_tile_size()

    def random_shuffle_ships(self):
        BaseBoard.random_shuffle_ships(self)
        self._update_ships_visual_position()

    def _update_ships_visual_position(self):
        for (row, col), ship_list in self.ships_map.items():
            for ship in ship_list:
                new_x, new_y = self.get_tile_screen_placement(row, col)
                ship.update_visual_position(new_x, new_y)

    def _update_single_ship_visual_position(self, ship):
        new_x, new_y = self.get_tile_screen_placement(ship.row, ship.col)
        ship.update_visual_position(new_x, new_y)

    def _draw_ships(self, window):
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

    def _populate_with_tiles(self):
        self.tiles = [
            [VisualTile(*self.get_tile_screen_placement(row, col)) for col in range(self.columns_count)]
            for row in range(self.rows_count)
        ]

    def _draw_tiles(self, window):
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
        return self.x <= pos_x <= self.get_right_border() and self.y <= pos_y <= self.get_bottom_border()

    def get_row_col_by_mouse(self, pos):
        pos_x, pos_y = pos
        tile_size = self.get_tile_size()
        row = (pos_y - self.y) // tile_size
        col = (pos_x - self.x) // tile_size
        return row, col

    def _draw_sunk_ships(self, window):
        for ship_list in self.ships_map.values():
            for ship in ship_list:
                if not ship.is_alive:
                    ship.set_color(colors.SHIP_SUNK_COLOR)
                    ship.draw(window)

    def _draw_hits(self, window):
        for row, col in self.all_hit_coordinates:
            tile = self.tiles[row][col]
            DrawUtils.draw_cross(window, tile.x, tile.y, tile.size, colors.SHOT_HIT_COLOR)

    def _draw_misses(self, window):
        for (row, col), hit_count in self.shot_coordinates.items():
            if hit_count > 0 and (row, col) not in self.all_hit_coordinates:
                tile = self.tiles[row][col]
                DrawUtils.draw_circle(window, tile.x, tile.y, tile.size, colors.SHOT_MISS_COLOR)

    def _draw_board_border(self, window):
        border_rect = pygame.Rect(
            self.x - self.BORDER_WIDTH,
            self.y - self.BORDER_WIDTH,
            self.get_right_border() - self.x + self.BORDER_WIDTH * 2,
            self.get_bottom_border() - self.y + self.BORDER_WIDTH * 2,
        )
        pygame.draw.rect(window, colors.BOARD_BORDER_COLOR, border_rect, self.BORDER_WIDTH)

    def _draw_numeration(self, window):
        font = pygame.font.SysFont(None, 22)
        tile_size = self.get_tile_size()

        for row in range(self.rows_count):
            number_text = font.render(str(row + 1), True, colors.BOARD_NUMERATION_COLOR)
            text_rect = number_text.get_rect(
                center=(
                    self.x - tile_size // 2,
                    self.y + row * tile_size + tile_size // 2,
                )
            )
            window.blit(number_text, text_rect.topleft)

        for col in range(self.columns_count):
            letter_text = font.render(chr(col + ord("A")), True, colors.BOARD_NUMERATION_COLOR)
            text_rect = letter_text.get_rect(
                center=(
                    self.x + col * tile_size + tile_size // 2,
                    self.y - tile_size // 2,
                )
            )
            window.blit(letter_text, text_rect.topleft)

    def draw(self, window):
        self._draw_board_border(window)
        self._draw_tiles(window)
        self._draw_numeration(window)

        self._draw_ships(window)
        self._draw_hits(window)
        self._draw_sunk_ships(window)
        self._draw_misses(window)

    def move_ship(self, ship, new_row, new_col, new_is_horizontal):
        BaseBoard.move_ship(self, ship, new_row, new_col, new_is_horizontal)
        self._update_single_ship_visual_position(ship)

    def place_ship(self, ship):
        BaseBoard.place_ship(self, ship)
        self._update_single_ship_visual_position(ship)

    def __repr__(self):
        return BaseBoard.__repr__(self)


class VisualBoardEnemyView(VisualBoard, BaseBoardEnemyView):
    def __init__(self, x=0, y=0):
        VisualBoard.__init__(self, x, y)
        BaseBoardEnemyView.__init__(self)

    def reveal_ship(self, ship, reveal_adjacent=False):
        visual_ship = VisualShip(
            ship.ship_length,
            ship.row,
            ship.col,
            ship.is_horizontal,
            ship.is_alive,
            ship.sunk_coordinates,
            coordinate_size=self.get_tile_size(),
        )
        BaseBoardEnemyView.reveal_ship(self, visual_ship, reveal_adjacent)
