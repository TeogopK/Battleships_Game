"""
This module provides a Button class and its derivatives for creating and handling interactive buttons in a Pygame application.
It includes features for rendering buttons with text, handling mouse interactions, and supporting different button states like hover and disabled.

The module also provides specialized button classes, such as `BasicButton` and `GoBackButton`, with pre-configured settings for common use cases.
"""

import pygame
import pygame.freetype
from game.visuals.utils import colors


class Button:
    """
    A class representing a clickable button in a Pygame application.
    """

    def __init__(
        self,
        x,
        y,
        text,
        font_size,
        width,
        height,
        padding=10,
        disabled=False,
    ):  # pylint: disable=R0913
        """
        Initializes a Button object with specified position, size, and text.

        Args:
            x (int): The x-coordinate of the top-left corner of the button.
            y (int): The y-coordinate of the top-left corner of the button.
            text (str): The text displayed on the button.
            font_size (int): The size of the font used for the button's text.
            width (int): The width of the button.
            height (int): The height of the button.
            padding (int, optional): The padding around the text inside the button. Defaults to 10.
            disabled (bool, optional): A flag indicating whether the button is disabled. Defaults to False.
        """
        self.font = pygame.freetype.SysFont("Arial", font_size)
        self.text = text
        self.width = width
        self.height = height
        self.padding = padding
        self.border_radius = 10
        self.disabled = disabled
        self.clicked = False

        self.text_color = colors.BUTTON_TEXT_COLOR
        self.bg_color = colors.BUTTON_BACKGROUND_COLOR
        self.hover_color = colors.BUTTON_HOVER_COLOR

        self.image, self.rect = self._create_text_surface(self.text, self.text_color)
        self.rect.topleft = (
            x + (self.width - self.rect.width) // 2,
            y + (self.height - self.rect.height) // 2,
        )
        self.rect.size = (self.rect.width, self.rect.height)

        self.button_rect = pygame.Rect(x, y, self.width, self.height)

    def _create_text_surface(self, text, color):
        """
        Creates a surface for the text with the specified color.

        Args:
            text (str): The text to be rendered on the button.
            color (tuple): The color of the text in RGB format.

        Returns:
            tuple: A tuple containing the text surface (pygame.Surface) and the text rectangle (pygame.Rect).
        """
        text_surface, rect = self.font.render(text, color)
        return text_surface, rect

    def draw(self, surface):
        """
        Draws the button on the specified surface, updating its appearance based on its state.

        Args:
            surface (pygame.Surface): The surface on which the button is drawn.
        """
        if self.disabled:
            bg_color = colors.BUTTON_DISABLED_COLOR
        else:
            pos = pygame.mouse.get_pos()
            mouse_over = self.button_rect.collidepoint(pos)
            bg_color = self.hover_color if mouse_over else self.bg_color

        pygame.draw.rect(surface, bg_color, self.button_rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, (0, 0, 0), self.button_rect, 2, border_radius=self.border_radius)
        self.image, _ = self._create_text_surface(self.text, self.text_color)
        text_x = self.button_rect.x + (self.button_rect.width - self.image.get_width()) // 2
        text_y = self.button_rect.y + (self.button_rect.height - self.image.get_height()) // 2
        surface.blit(self.image, (text_x, text_y))

    def is_active(self):
        """
        Checks if the button is currently active (i.e., if it's clicked while not being disabled).

        Returns:
            bool: True if the button is active and clicked, False otherwise.
        """
        if self.disabled:
            return False

        pos = pygame.mouse.get_pos()
        mouse_over = self.button_rect.collidepoint(pos)

        if mouse_over and pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            return True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return False

    def set_disabled(self, disabled):
        """
        Sets the disabled state of the button.

        Args:
            disabled (bool): A flag indicating whether to disable (True) or enable (False) the button.
        """
        self.disabled = disabled


class BasicButton(Button):
    """
    A basic button with default settings suitable for general use.
    Inherits from the Button class with pre-configured width, height, and font size.

    Attributes:
        x (int): The x-coordinate of the top-left corner of the button.
        y (int): The y-coordinate of the top-left corner of the button.
        text (str): The text displayed on the button.
        width (int): The width of the button (default 300).
    """

    def __init__(self, x, y, text, width=300):
        """
        Initializes a BasicButton object with specified position and text, and default width.

        Args:
            x (int): The x-coordinate of the top-left corner of the button.
            y (int): The y-coordinate of the top-left corner of the button.
            text (str): The text displayed on the button.
            width (int, optional): The width of the button. Defaults to 300.
        """
        super().__init__(
            x,
            y,
            text=text,
            font_size=30,
            width=width,
            height=50,
            padding=20,
        )


class GoBackButton(Button):
    """
    A specific button designed for "Go back" functionality.
    Inherits from the Button class with a smaller size and pre-configured text.

    Attributes:
        x (int): The x-coordinate of the top-left corner of the button.
        y (int): The y-coordinate of the top-left corner of the button.
    """

    def __init__(self, x, y):
        """
        Initializes a GoBackButton object with specified position and pre-configured settings.

        Args:
            x (int): The x-coordinate of the top-left corner of the button.
            y (int): The y-coordinate of the top-left corner of the button.
        """
        super().__init__(
            x,
            y,
            text="Go back",
            font_size=22,
            width=100,
            height=30,
            padding=10,
        )
