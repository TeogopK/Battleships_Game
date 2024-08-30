import pygame
import pygame.freetype
from game.visuals.utils import colors


class Button:
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

        self.image, self.rect = self.create_text_surface(self.text, self.text_color)
        self.rect.topleft = (
            x + (self.width - self.rect.width) // 2,
            y + (self.height - self.rect.height) // 2,
        )
        self.rect.size = (self.rect.width, self.rect.height)

        self.button_rect = pygame.Rect(x, y, self.width, self.height)

    def create_text_surface(self, text, color):
        text_surface, rect = self.font.render(text, color)
        return text_surface, rect

    def draw(self, surface):
        if self.disabled:
            bg_color = colors.BUTTON_DISABLED_COLOR
        else:
            pos = pygame.mouse.get_pos()
            mouse_over = self.button_rect.collidepoint(pos)
            bg_color = self.hover_color if mouse_over else self.bg_color

        pygame.draw.rect(surface, bg_color, self.button_rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, (0, 0, 0), self.button_rect, 2, border_radius=self.border_radius)
        self.image, _ = self.create_text_surface(self.text, self.text_color)
        text_x = self.button_rect.x + (self.button_rect.width - self.image.get_width()) // 2
        text_y = self.button_rect.y + (self.button_rect.height - self.image.get_height()) // 2
        surface.blit(self.image, (text_x, text_y))

    def is_active(self):
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
        self.disabled = disabled


class BasicButton(Button):
    def __init__(self, x, y, text, width=300):
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
    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            text="Go back",
            font_size=22,
            width=100,
            height=30,
            padding=10,
        )
