import pygame
from pygame.sprite import Sprite

from game.visuals.utils.constants import RESOLUTION
from game.interface.base_board import Ship
import game.visuals.utils.colors as colors


class Visual_Ship(Sprite, Ship):
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
    ):
        Ship.__init__(
            self, ship_length, row, col, is_horizontal, is_alive, sunk_coordinates
        )
        Sprite.__init__(self)
        self.coordinate_size = coordinate_size
        self.x = x
        self.y = y
        self.color = colors.SHIP_DEFAULT_COLOR

    def get_visual_length(self):
        return (
            self.ship_length * self.coordinate_size
            if self.is_horizontal
            else self.coordinate_size
        )

    def get_visual_width(self):
        return (
            self.coordinate_size
            if self.is_horizontal
            else self.ship_length * self.coordinate_size
        )

    def get_right_border(self):
        return self.x + self.get_visual_length()

    def get_bottom_border(self):
        return self.y + self.coordinate_size

    def update_visual_position(self, x, y):
        self.x = x
        self.y = y

    def set_color(self, color):
        self.color = color

    def draw(self, window):
        ship_position = (
            self.x,
            self.y,
            self.get_visual_length(),
            self.get_visual_width(),
        )
        pygame.draw.rect(window, self.color, ship_position)
        pygame.draw.rect(window, colors.SHIP_BORDER_COLOR, ship_position, 3)

    def __repr__(self):
        return Ship.__repr__(self)
