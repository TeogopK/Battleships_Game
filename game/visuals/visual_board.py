"""
This module defines classes for the visual representation of the game board and tiles using Pygame.
It includes the `VisualTile`, `VisualBoard`, and `VisualBoardEnemyView` classes, which extend base game logic
classes and integrate graphical rendering.
"""

import pygame
from pygame.sprite import Sprite

from game.visuals.utils.constants import RESOLUTION
from game.interface.base_board import BaseBoard, BaseBoardEnemyView
from game.visuals.visual_ship import VisualShip

from game.visuals.utils import colors
from game.visuals.utils.draw_utils import DrawUtils


class VisualTile(Sprite):
    """
    A class representing a single tile on the visual game board.

    Attributes:
        TILE_SIZE (int): The base size of a tile before applying resolution scaling.
        x (int): The x-coordinate of the tile's top-left corner.
        y (int): The y-coordinate of the tile's top-left corner.
        size (int): The size of the tile in pixels, adjusted for screen resolution.
        is_hovered (bool): Whether the tile is currently being hovered over by the mouse.
    """

    TILE_SIZE = 50

    def __init__(self, x, y):
        """
        Initializes a VisualTile object with the specified position.

        Args:
            x (int): The x-coordinate for the tile's top-left corner.
            y (int): The y-coordinate for the tile's top-left corner.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.size = self.TILE_SIZE * RESOLUTION
        self.is_hovered = False

    def get_size(self):
        """
        Returns the size of the tile in pixels.

        Returns:
            int: The size of the tile.
        """
        return self.size

    def draw_tile(self, window):
        """
        Draws the tile on the provided Pygame window surface.

        Args:
            window (pygame.Surface): The surface on which to draw the tile.
        """
        tile_position = (self.x, self.y, self.size, self.size)
        tile_color = colors.TILE_HOVER_COLOR if self.is_hovered else colors.TILE_MAIN_COLOR
        pygame.draw.rect(window, tile_color, tile_position)
        pygame.draw.rect(window, colors.TILE_BORDER_COLOR, tile_position, 1)

    def set_hover(self, is_hovered):
        """
        Sets whether the tile is currently hovered over by the mouse.

        Args:
            is_hovered (bool): True if the tile is hovered, False otherwise.
        """
        self.is_hovered = is_hovered

    def __repr__(self):
        """
        Returns a string representation of the VisualTile object.

        Returns:
            str: A string that represents the VisualTile's position.
        """
        return f"<Tile at {self.x}, {self.y}>"


class VisualBoard(Sprite, BaseBoard):
    """
    A class representing the visual game board, extending both Sprite and BaseBoard.
    """

    BORDER_WIDTH = 5

    def __init__(self, x=0, y=0):
        """
        Initializes a VisualBoard object with the specified position.

        Args:
            x (int, optional): The x-coordinate for the board's top-left corner. Defaults to 0.
            y (int, optional): The y-coordinate for the board's top-left corner. Defaults to 0.
        """
        BaseBoard.__init__(self, ship_constructor=VisualShip)
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.tiles = []
        self._populate_with_tiles()

        self._initialize_visual_ships()
        self.random_shuffle_ships()

    def _initialize_visual_ships(self):
        """
        Initializes the visual representation of the ships on the board.
        """
        for ship in self.unplaced_ships:
            ship.coordinate_size = self.get_tile_size()

    def random_shuffle_ships(self):
        """
        Randomly shuffles the ships on the board and updates their visual positions.
        """
        BaseBoard.random_shuffle_ships(self)
        self._update_ships_visual_position()

    def _update_ships_visual_position(self):
        """
        Updates the visual positions of all ships on the board based on their logical positions.
        """
        for (row, col), ship_list in self.ships_map.items():
            for ship in ship_list:
                new_x, new_y = self.get_tile_screen_placement(row, col)
                ship.update_visual_position(new_x, new_y)

    def _update_single_ship_visual_position(self, ship):
        """
        Updates the visual position of a single ship on the board.

        Args:
            ship (VisualShip): The ship whose visual position needs to be updated.
        """
        new_x, new_y = self.get_tile_screen_placement(ship.row, ship.col)
        ship.update_visual_position(new_x, new_y)

    def _draw_ships(self, window):
        """
        Draws all ships on the board, both placed and unplaced, on the provided Pygame window surface.

        Args:
            window (pygame.Surface): The surface on which to draw the ships.
        """
        for ship_list in self.ships_map.values():
            for ship in ship_list:
                ship.draw(window)

        for ship in self.unplaced_ships:
            ship.draw(window)

    def get_tile_screen_placement(self, row, col):
        """
        Calculates the screen coordinates of a tile based on its row and column on the board.

        Args:
            row (int): The row of the tile.
            col (int): The column of the tile.

        Returns:
            tuple: A tuple containing the x and y screen coordinates of the tile.
        """
        return (
            self.x + col * VisualTile.TILE_SIZE,
            self.y + row * VisualTile.TILE_SIZE,
        )

    def _populate_with_tiles(self):
        """
        Populates the board with tiles based on its dimensions.
        """
        self.tiles = [
            [VisualTile(*self.get_tile_screen_placement(row, col)) for col in range(self.columns_count)]
            for row in range(self.rows_count)
        ]

    def _draw_tiles(self, window):
        """
        Draws all tiles on the board on the provided Pygame window surface.

        Args:
            window (pygame.Surface): The surface on which to draw the tiles.
        """
        for row in range(self.rows_count):
            for col in range(self.columns_count):
                tile = self.tiles[row][col]
                tile.draw_tile(window)

    def get_tile_size(self):
        """
        Returns the size of a single tile on the board.

        Returns:
            int: The size of the tile.
        """
        return self.tiles[0][0].get_size()

    def get_right_border(self):
        """
        Calculates the x-coordinate of the right border of the board.

        Returns:
            int: The x-coordinate of the board's right border.
        """
        return self.x + len(self.tiles) * self.get_tile_size()

    def get_bottom_border(self):
        """
        Calculates the y-coordinate of the bottom border of the board.

        Returns:
            int: The y-coordinate of the board's bottom border.
        """
        return self.y + len(self.tiles) * self.get_tile_size()

    def is_position_in_board(self, pos):
        """
        Checks whether a given position is within the boundaries of the board.

        Args:
            pos (tuple): A tuple containing the x and y coordinates of the position.

        Returns:
            bool: True if the position is within the board, False otherwise.
        """
        pos_x, pos_y = pos
        return self.x <= pos_x <= self.get_right_border() and self.y <= pos_y <= self.get_bottom_border()

    def get_row_col_by_mouse(self, pos):
        """
        Calculates the row and column on the board based on a mouse position.

        Args:
            pos (tuple): A tuple containing the x and y coordinates of the mouse position.

        Returns:
            tuple: A tuple containing the row and column corresponding to the mouse position.
        """
        pos_x, pos_y = pos
        tile_size = self.get_tile_size()
        row = (pos_y - self.y) // tile_size
        col = (pos_x - self.x) // tile_size
        return row, col

    def _draw_sunk_ships(self, window):
        """
        Draws the sunk ships on the board with a special color.

        Args:
            window (pygame.Surface): The surface on which to draw the sunk ships.
        """
        for ship_list in self.ships_map.values():
            for ship in ship_list:
                if not ship.is_alive:
                    ship.set_color(colors.SHIP_SUNK_COLOR)
                    ship.draw(window)

    def _draw_hits(self, window):
        """
        Draws the hit marks on the board where ships have been hit.

        Args:
            window (pygame.Surface): The surface on which to draw the hit marks.
        """
        for row, col in self.all_hit_coordinates:
            tile = self.tiles[row][col]
            DrawUtils.draw_cross(window, tile.x, tile.y, tile.size, colors.SHOT_HIT_COLOR)

    def _draw_misses(self, window):
        """
        Draws the miss marks on the board where shots did not hit any ships.

        Args:
            window (pygame.Surface): The surface on which to draw the miss marks.
        """
        for (row, col), hit_count in self.shot_coordinates.items():
            if hit_count > 0 and (row, col) not in self.all_hit_coordinates:
                tile = self.tiles[row][col]
                DrawUtils.draw_circle(window, tile.x, tile.y, tile.size, colors.SHOT_MISS_COLOR)

    def _draw_board_border(self, window):
        """
        Draws the border around the game board.

        Args:
            window (pygame.Surface): The surface on which to draw the board border.
        """
        border_rect = pygame.Rect(
            self.x - self.BORDER_WIDTH,
            self.y - self.BORDER_WIDTH,
            self.get_right_border() - self.x + self.BORDER_WIDTH * 2,
            self.get_bottom_border() - self.y + self.BORDER_WIDTH * 2,
        )
        pygame.draw.rect(window, colors.BOARD_BORDER_COLOR, border_rect, self.BORDER_WIDTH)

    def _draw_numeration(self, window):
        """
        Draws the numeration (row and column labels) around the board.

        Args:
            window (pygame.Surface): The surface on which to draw the numeration.
        """
        font = pygame.font.SysFont(None, 22)
        tile_size = self.get_tile_size()

        # Draw row numeration
        for row in range(self.rows_count):
            number_text = font.render(str(row + 1), True, colors.BOARD_NUMERATION_COLOR)
            text_rect = number_text.get_rect(
                center=(
                    self.x - tile_size // 2,
                    self.y + row * tile_size + tile_size // 2,
                )
            )
            window.blit(number_text, text_rect.topleft)

        # Draw column numeration
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
        """
        Draws the entire visual board, including tiles, numeration, ships, hits, misses, and borders.

        Args:
            window (pygame.Surface): The surface on which to draw the entire board.
        """
        self._draw_board_border(window)
        self._draw_tiles(window)
        self._draw_numeration(window)

        self._draw_ships(window)
        self._draw_hits(window)
        self._draw_sunk_ships(window)
        self._draw_misses(window)

    def move_ship(self, ship, new_row, new_col, new_is_horizontal):
        """
        Moves a ship to a new position on the board and updates its visual position.

        Args:
            ship (VisualShip): The ship to move.
            new_row (int): The new row for the ship.
            new_col (int): The new column for the ship.
            new_is_horizontal (bool): Whether the ship is horizontal in the new position.
        """
        BaseBoard.move_ship(self, ship, new_row, new_col, new_is_horizontal)
        self._update_single_ship_visual_position(ship)

    def place_ship(self, ship):
        """
        Places a ship on the board and updates its visual position.

        Args:
            ship (VisualShip): The ship to place.
        """
        BaseBoard.place_ship(self, ship)
        self._update_single_ship_visual_position(ship)

    def __repr__(self):
        """
        Returns a string representation of the VisualBoard object, delegating to the base class.

        Returns:
            str: A string that represents the VisualBoard's state.
        """
        return BaseBoard.__repr__(self)


class VisualBoardEnemyView(VisualBoard, BaseBoardEnemyView):
    """
    A class representing the enemy view of the visual game board. Inherits from VisualBoard and BaseBoardEnemyView.

    Inherits:
        VisualBoard: Provides visual representation of the board.
        BaseBoardEnemyView: Provides enemy view logic and interactions.
    """

    def __init__(self, x=0, y=0):
        """
        Initializes a VisualBoardEnemyView object with the specified position.

        Args:
            x (int, optional): The x-coordinate for the board's top-left corner. Defaults to 0.
            y (int, optional): The y-coordinate for the board's top-left corner. Defaults to 0.
        """
        VisualBoard.__init__(self, x, y)
        BaseBoardEnemyView.__init__(self)

    def reveal_ship(self, ship, reveal_adjacent=False):
        """
        Reveals a ship on the enemy's board and optionally reveals adjacent tiles.

        Args:
            ship (Ship): The ship to reveal.
            reveal_adjacent (bool, optional): Whether to reveal adjacent tiles. Defaults to False.
        """
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
