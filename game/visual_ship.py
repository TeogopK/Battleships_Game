import pygame
from pygame.sprite import Sprite

from constants import RESOLUTION
from base_board import Ship


class Visual_Ship(Sprite, Ship):
    def __init__(self, ship_length, coordinate_size=None, x=None, y=None):
        Ship.__init__(self, ship_length)
        Sprite.__init__(self)
        self.coordinate_size = coordinate_size
        self.x = x
        self.y = y

    def get_visual_length(self):
        return self.ship_length * self.coordinate_size if self.is_horizontal else self.coordinate_size

    def get_visual_width(self):
        return self.coordinate_size if self.is_horizontal else self.ship_length * self.coordinate_size

    def get_right_border(self):
        return self.x + self.get_visual_length()

    def get_bottom_border(self):
        return self.y + self.coordinate_size

    def update_visual_position(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        ship_position = (self.x,
                         self.y, self.get_visual_length(), self.get_visual_width())
        pygame.draw.rect(window, (29, 53, 87), ship_position)
        pygame.draw.rect(window, (0, 100, 0), ship_position, 1)
