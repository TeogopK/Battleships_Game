"""
This module provides utility functions for drawing various graphical elements using Pygame.
It includes functions to draw crosses, circles, text, and pop-up messages on a Pygame surface,
as well as applying effects like blur and color overlays.
"""

import pygame
from game.visuals.utils import colors


class DrawUtils:
    """
    A collection of static utility methods for drawing various elements on a Pygame surface.
    These methods include drawing crosses, circles, text, and applying visual effects like blurring
    and color overlays.
    """

    @staticmethod
    def draw_cross(surface, top_left_x, top_left_y, size, color, line_thickness=5):
        """
        Draws a cross (X) on the specified surface.

        Args:
            surface (pygame.Surface): The surface to draw the cross on.
            top_left_x (int): The x-coordinate of the top-left corner of the cross's bounding box.
            top_left_y (int): The y-coordinate of the top-left corner of the cross's bounding box.
            size (int): The size (both width and height) of the cross's bounding box.
            color (tuple): The color of the cross in RGB format.
            line_thickness (int, optional): The thickness of the cross lines. Defaults to 5.
        """
        center_x = top_left_x + size // 2
        center_y = top_left_y + size // 2
        half_size = size // 3

        pygame.draw.line(
            surface,
            color,
            (center_x - half_size, center_y - half_size),
            (center_x + half_size, center_y + half_size),
            line_thickness,
        )

        pygame.draw.line(
            surface,
            color,
            (center_x - half_size, center_y + half_size),
            (center_x + half_size, center_y - half_size),
            line_thickness,
        )

    @staticmethod
    def draw_circle(surface, top_left_x, top_left_y, size, color):
        """
        Draws a circle on the specified surface.

        Args:
            surface (pygame.Surface): The surface to draw the circle on.
            top_left_x (int): The x-coordinate of the top-left corner of the circle's bounding box.
            top_left_y (int): The y-coordinate of the top-left corner of the circle's bounding box.
            size (int): The diameter of the circle's bounding box.
            color (tuple): The color of the circle in RGB format.
        """
        pygame.draw.circle(surface, color, (top_left_x + size // 2, top_left_y + size // 2), size // 4)

    @staticmethod
    def draw_title(surface, text, x, y, font_size, glow_size):
        """
        Draws a title with a glow effect on the specified surface.

        Args:
            surface (pygame.Surface): The surface to draw the title on.
            text (str): The text of the title.
            x (int): The x-coordinate of the title's center.
            y (int): The y-coordinate of the title's center.
            font_size (int): The size of the font to be used for the title.
            glow_size (int): The size of the glow effect around the title.
        """
        main_color = colors.TITLE_TEXT_COLOR
        glow_color = colors.TITLE_SHADOW_COLOR

        font = pygame.font.Font(None, font_size)

        text_surface = font.render(text, True, main_color)
        glow_surface = font.render(text, True, glow_color)

        text_rect = text_surface.get_rect(center=(x, y))

        for offset in range(1, glow_size):
            surface.blit(glow_surface, text_rect.move(-offset, 0))
            surface.blit(glow_surface, text_rect.move(offset, 0))
            surface.blit(glow_surface, text_rect.move(0, -offset))
            surface.blit(glow_surface, text_rect.move(0, offset))

        surface.blit(text_surface, text_rect)

    @staticmethod
    def draw_text(
        surface,
        text,
        x,
        y,
        font_size,
        text_color=colors.TEXT_LABEL_COLOR,
        alignment="center",
    ):
        """
        Draws text on the specified surface with the given alignment.

        Args:
            surface (pygame.Surface): The surface to draw the text on.
            text (str): The text to be displayed.
            x (int): The x-coordinate for text alignment.
            y (int): The y-coordinate for text alignment.
            font_size (int): The size of the font to be used for the text.
            text_color (tuple, optional): The color of the text in RGB format. Defaults to colors.TEXT_LABEL_COLOR.
            alignment (str, optional): The alignment of the text ('left', 'center', 'right'). Defaults to 'center'.
        """
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, text_color)

        if alignment == "left":
            text_rect = text_surface.get_rect(left=x, centery=y)
        elif alignment == "right":
            text_rect = text_surface.get_rect(right=x, centery=y)
        else:
            text_rect = text_surface.get_rect(center=(x, y))

        surface.blit(text_surface, text_rect)

    @staticmethod
    def draw_input_text(
        surface,
        text,
        x,
        y,
        font_size=46,
        text_color=colors.TEXT_INPUT_COLOR,
        alignment="center",
    ):
        """
        Draws input text on the specified surface with the given alignment.

        Args:
            surface (pygame.Surface): The surface to draw the input text on.
            text (str): The input text to be displayed.
            x (int): The x-coordinate for text alignment.
            y (int): The y-coordinate for text alignment.
            font_size (int, optional): The size of the font to be used for the text. Defaults to 46.
            text_color (tuple, optional): The color of the text in RGB format. Defaults to colors.TEXT_INPUT_COLOR.
            alignment (str, optional): The alignment of the text ('left', 'center', 'right'). Defaults to 'center'.
        """
        DrawUtils.draw_text(surface, text, x, y, font_size, text_color, alignment)

    @staticmethod
    def draw_label(
        surface,
        text,
        x,
        y,
        font_size=36,
        text_color=colors.TEXT_LABEL_COLOR,
        alignment="center",
    ):
        """
        Draws a label on the specified surface with the given alignment.

        Args:
            surface (pygame.Surface): The surface to draw the label on.
            text (str): The label text to be displayed.
            x (int): The x-coordinate for text alignment.
            y (int): The y-coordinate for text alignment.
            font_size (int, optional): The size of the font to be used for the label. Defaults to 36.
            text_color (tuple, optional): The color of the label text in RGB format. Defaults to colors.TEXT_LABEL_COLOR.
            alignment (str, optional): The alignment of the text ('left', 'center', 'right'). Defaults to 'center'.
        """
        DrawUtils.draw_text(surface, text, x, y, font_size, text_color, alignment)

    @staticmethod
    def draw_message(
        surface,
        text,
        x,
        y,
        font_size=24,
        text_color=colors.TEXT_MESSAGE_COLOR,
        alignment="center",
    ):
        """
        Draws a message on the specified surface with the given alignment.

        Args:
            surface (pygame.Surface): The surface to draw the message on.
            text (str): The message text to be displayed.
            x (int): The x-coordinate for text alignment.
            y (int): The y-coordinate for text alignment.
            font_size (int, optional): The size of the font to be used for the message. Defaults to 24.
            text_color (tuple, optional): The color of the message text in RGB format. Defaults to colors.TEXT_MESSAGE_COLOR.
            alignment (str, optional): The alignment of the text ('left', 'center', 'right'). Defaults to 'center'.
        """
        DrawUtils.draw_text(surface, text, x, y, font_size, text_color, alignment)

    @staticmethod
    def apply_blur(surface, scale_factor=0.1):
        """
        Applies a blur effect to the specified surface.

        Args:
            surface (pygame.Surface): The surface to which the blur effect will be applied.
            scale_factor (float, optional): The factor by which the surface is scaled down before being scaled back up. Defaults to 0.1.
        """
        width, height = surface.get_size()

        small_surface = pygame.transform.smoothscale(surface, (int(width * scale_factor), int(height * scale_factor)))

        blurred_surface = pygame.transform.smoothscale(small_surface, (width, height))

        surface.blit(blurred_surface, (0, 0))

    @staticmethod
    def apply_color_overlay(screen, color=colors.BACKGROUND_COLOR, alpha=128):
        """
        Applies a color overlay with transparency to the specified surface.

        Args:
            screen (pygame.Surface): The surface to which the color overlay will be applied.
            color (tuple, optional): The color of the overlay in RGB format. Defaults to colors.BACKGROUND_COLOR.
            alpha (int, optional): The alpha transparency level of the overlay (0-255). Defaults to 128.
        """
        overlay_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay_surface.fill((*color, alpha))

        screen.blit(overlay_surface, (0, 0))

    @staticmethod
    def draw_popup_centered_message(
        surface,
        title_text,
        subtitle_text,
        font_size_title=64,
        font_size_subtitle=30,
        alpha=228,
    ):  # pylint: disable=R0914
        """
        Draws a centered pop-up message with a title and subtitle on the specified surface.

        Args:
            surface (pygame.Surface): The surface to draw the pop-up message on.
            title_text (str): The title text to be displayed.
            subtitle_text (str): The subtitle text to be displayed.
            font_size_title (int, optional): The size of the font to be used for the title. Defaults to 64.
            font_size_subtitle (int, optional): The size of the font to be used for the subtitle. Defaults to 30.
            alpha (int, optional): The alpha transparency level of the pop-up background (0-255). Defaults to 228.
        """
        # Define default values
        background_color = colors.TEXTBOX_BACKGROUND_COLOR
        text_color_title = colors.TITLE_TEXT_COLOR
        text_color_subtitle = colors.TEXT_LABEL_COLOR
        border_color = colors.TEXTBOX_BORDER_COLOR
        padding = 20
        border_width = 2

        # Create text surfaces
        font_title = pygame.font.SysFont(None, font_size_title)
        font_subtitle = pygame.font.SysFont(None, font_size_subtitle)

        # Render text surfaces
        title_text_surface = font_title.render(title_text, True, text_color_title)
        subtitle_text_surface = font_subtitle.render(subtitle_text, True, text_color_subtitle)

        # Calculate rectangle dimensions and position
        text_width = max(title_text_surface.get_width(), subtitle_text_surface.get_width())
        rect_width = text_width + padding * 2
        rect_height = title_text_surface.get_height() + subtitle_text_surface.get_height() + padding * 3
        rect_x = (surface.get_width() - rect_width) // 2
        rect_y = (surface.get_height() - rect_height) // 2

        # Create and draw on message surface
        message_surface = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        pygame.draw.rect(
            message_surface,
            (*background_color, alpha),
            (rect_x, rect_y, rect_width, rect_height),
            border_radius=15,
        )
        pygame.draw.rect(
            message_surface,
            border_color,
            (rect_x, rect_y, rect_width, rect_height),
            border_radius=15,
            width=border_width,
        )

        # Draw text
        surface.blit(message_surface, (0, 0))
        title_rect = title_text_surface.get_rect(center=(rect_x + rect_width // 2, rect_y + padding + font_size_title // 2))
        subtitle_rect = subtitle_text_surface.get_rect(
            center=(
                rect_x + rect_width // 2,
                rect_y + rect_height - padding - font_size_subtitle // 2,
            )
        )
        surface.blit(title_text_surface, title_rect)
        surface.blit(subtitle_text_surface, subtitle_rect)
