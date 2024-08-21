import pygame
import game.visuals.utils.colors as colors


class DrawUtils:
    @staticmethod
    def draw_cross(surface, top_left_x, top_left_y, size, color, line_thickness=5):
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
        Draws a miss mark on the given surface at the top-left coordinate (top_left_x, y)
        with the specified size and color.
        """
        pygame.draw.circle(
            surface, color, (top_left_x + size // 2, top_left_y + size // 2), size // 4
        )

    @staticmethod
    def draw_title(surface, text, x, y, font_size, glow_size):
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
        DrawUtils.draw_text(surface, text, x, y, font_size, text_color, alignment)
