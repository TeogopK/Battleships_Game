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

    @staticmethod
    def draw_centered_message_with_background(
        surface,
        title_text,
        subtitle_text,
        font_size_title=64,
        font_size_subtitle=30,
        background_color=colors.TEXTBOX_BACKGROUND_COLOR,
        text_color_title=colors.TITLE_TEXT_COLOR,
        text_color_subtitle=colors.TEXT_LABEL_COLOR,
        padding=20,
        border_color=colors.TEXTBOX_BORDER_COLOR,
        border_width=2,
        alpha=228,
    ):
        message_surface = pygame.Surface(
            (surface.get_width(), surface.get_height()), pygame.SRCALPHA
        )

        # Calculate rectangle dimensions and position
        font_title = pygame.font.SysFont(None, font_size_title)
        font_subtitle = pygame.font.SysFont(None, font_size_subtitle)

        title_text_surface = font_title.render(title_text, True, text_color_title)
        subtitle_text_surface = font_subtitle.render(
            subtitle_text, True, text_color_subtitle
        )

        rect_width = (
            max(title_text_surface.get_width(), subtitle_text_surface.get_width())
            + padding * 2
        )
        rect_height = (
            title_text_surface.get_height()
            + subtitle_text_surface.get_height()
            + padding * 3
        )
        rect_x = (surface.get_width() - rect_width) // 2
        rect_y = (surface.get_height() - rect_height) // 2

        # Draw semi-transparent background rectangle on the message surface
        pygame.draw.rect(
            message_surface,
            (background_color[0], background_color[1], background_color[2], alpha),
            (rect_x, rect_y, rect_width, rect_height),
            border_radius=15,
        )

        # Draw border around the rectangle
        pygame.draw.rect(
            message_surface,
            border_color,
            (rect_x, rect_y, rect_width, rect_height),
            border_radius=15,
            width=border_width,
        )

        # Draw text directly onto the main surface
        surface.blit(message_surface, (0, 0))
        surface.blit(
            title_text_surface,
            title_text_surface.get_rect(
                center=(
                    rect_x + rect_width // 2,
                    rect_y + padding + font_size_title // 2,
                )
            ),
        )
        surface.blit(
            subtitle_text_surface,
            subtitle_text_surface.get_rect(
                center=(
                    rect_x + rect_width // 2,
                    rect_y + rect_height - padding - font_size_subtitle // 2,
                )
            ),
        )

    def apply_blur(surface, scale_factor=0.1, blur_factor=2):
        width, height = surface.get_size()

        small_surface = pygame.transform.smoothscale(
            surface, (int(width * scale_factor), int(height * scale_factor))
        )

        blurred_surface = pygame.transform.smoothscale(small_surface, (width, height))

        surface.blit(blurred_surface, (0, 0))

    def apply_color_overlay(screen, color=colors.BACKGROUND_COLOR, alpha=128):
        # Create an overlay surface with the same size as the screen
        overlay_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        # Fill the overlay surface with the color and alpha
        overlay_surface.fill((*color, alpha))

        # Blit the overlay surface on top of the screen
        screen.blit(overlay_surface, (0, 0))
