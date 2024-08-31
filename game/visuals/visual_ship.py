"""
This module defines the `VisualShip` class, which represents a ship on a graphical game board.
It extends both `pygame.sprite.Sprite` and a base `Ship` class, integrating the ship's logical properties
with visual representation and rendering using Pygame.
"""

import pygame
from pygame.sprite import Sprite

from game.interface.base_board import Ship
from game.visuals.utils import colors


class VisualShip(Sprite, Ship):
    """
    A class that represents a visual representation of a ship in the game.

    Inherits from both the `Ship` class, which contains the logical properties of a ship, and
    `pygame.sprite.Sprite`, which allows the ship to be treated as a sprite within Pygame's framework.
    """

    def __init__(
        self,
        ship_length,
        row=None,
        col=None,
        is_horizontal=True,
        is_alive=True,
        sunk_coordinates=None,
        coordinate_size=None,
        x=None,
        y=None,
    ):  # pylint: disable=R0913
        """
        Initializes a VisualShip object with the specified properties.

        Args:
            ship_length (int): The length of the ship.
            row (int, optional): The starting row of the ship on the board grid. Defaults to None.
            col (int, optional): The starting column of the ship on the board grid. Defaults to None.
            is_horizontal (bool, optional): Orientation of the ship. True if horizontal, False if vertical.
                Defaults to True.
            is_alive (bool, optional): Whether the ship is still afloat. Defaults to True.
            sunk_coordinates (list, optional): The coordinates of the parts of the ship that have been sunk.
                Defaults to None.
            coordinate_size (int, optional): The size of a single grid coordinate in pixels. Defaults to None.
            x (int, optional): The x-coordinate for the ship's top-left corner on the screen. Defaults to None.
            y (int, optional): The y-coordinate for the ship's top-left corner on the screen. Defaults to None.
        """
        Ship.__init__(self, ship_length, row, col, is_horizontal, is_alive, sunk_coordinates)
        Sprite.__init__(self)
        self.coordinate_size = coordinate_size
        self.x = x
        self.y = y
        self.color = colors.SHIP_DEFAULT_COLOR

    def get_visual_length(self):
        """
        Returns the visual length of the ship in pixels, based on its orientation.

        Returns:
            int: The length of the ship in pixels if horizontal, or the width in pixels if vertical.
        """
        return self.ship_length * self.coordinate_size if self.is_horizontal else self.coordinate_size

    def get_visual_width(self):
        """
        Returns the visual width of the ship in pixels, based on its orientation.

        Returns:
            int: The width of the ship in pixels if horizontal, or the length in pixels if vertical.
        """
        return self.coordinate_size if self.is_horizontal else self.ship_length * self.coordinate_size

    def get_right_border(self):
        """
        Calculates the x-coordinate of the right border of the ship.

        Returns:
            int: The x-coordinate of the ship's right border.
        """
        return self.x + self.get_visual_length()

    def get_bottom_border(self):
        """
        Calculates the y-coordinate of the bottom border of the ship.

        Returns:
            int: The y-coordinate of the ship's bottom border.
        """
        return self.y + self.get_visual_width()

    def update_visual_position(self, x, y):
        """
        Updates the visual position of the ship on the screen.

        Args:
            x (int): The new x-coordinate for the ship's top-left corner.
            y (int): The new y-coordinate for the ship's top-left corner.
        """
        self.x = x
        self.y = y

    def set_color(self, color):
        """
        Sets the color of the ship for rendering.

        Args:
            color (tuple): The new color for the ship, represented as an RGB tuple.
        """
        self.color = color

    def draw(self, window):
        """
        Draws the ship on the given Pygame window surface.

        Args:
            window (pygame.Surface): The surface on which to draw the ship.
        """
        ship_position = (
            self.x,
            self.y,
            self.get_visual_length(),
            self.get_visual_width(),
        )
        pygame.draw.rect(window, self.color, ship_position)
        pygame.draw.rect(window, colors.SHIP_BORDER_COLOR, ship_position, 3)

    def __repr__(self):
        """
        Returns a string representation of the VisualShip object.

        Returns:
            str: A string that represents the current state of the VisualShip object.
        """
        return Ship.__repr__(self)
