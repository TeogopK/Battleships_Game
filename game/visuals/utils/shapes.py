import pygame


class DrawUtils:
    @staticmethod
    def draw_cross(surface, top_left_x, top_left_y, size, color, line_thickness=5):
        center_x = top_left_x + size // 2
        center_y = top_left_y + size // 2
        half_size = size // 3

        pygame.draw.line(
            surface, color,
            (center_x - half_size, center_y - half_size),
            (center_x + half_size, center_y + half_size),
            line_thickness
        )

        pygame.draw.line(
            surface, color,
            (center_x - half_size, center_y + half_size),
            (center_x + half_size, center_y - half_size),
            line_thickness
        )

    @staticmethod
    def draw_circle(surface, top_left_x, top_left_y, size, color):
        """
        Draws a miss mark on the given surface at the top-left coordinate (top_left_x, y)
        with the specified size and color.
        """
        pygame.draw.circle(
            surface, color,
            (top_left_x + size // 2, top_left_y + size // 2),
            size // 4
        )
