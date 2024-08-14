import pygame
import pygame.freetype
import game.visuals.utils.colors as colors


class Button:
    def __init__(self, x, y, text, font_size, text_color, bg_color, hover_color, width, height, padding=10, border_radius=5):
        self.font = pygame.freetype.SysFont("Arial", font_size)
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.width = width
        self.height = height
        self.padding = padding
        self.border_radius = border_radius
        self.clicked = False

        self.image, self.rect = self.create_text_surface(text, text_color)
        self.rect.topleft = (x + (width - self.rect.width) // 2, y + (height - self.rect.height) // 2)
        self.rect.size = (self.rect.width, self.rect.height)

        self.button_rect = pygame.Rect(x, y, width, height)

    def create_text_surface(self, text, color):
        text_surface, rect = self.font.render(text, color)
        return text_surface, rect

    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        mouse_over = self.button_rect.collidepoint(pos)

        bg_color = self.hover_color if mouse_over else self.bg_color
        pygame.draw.rect(surface, bg_color, self.button_rect, border_radius=self.border_radius)

        pygame.draw.rect(surface, (0, 0, 0), self.button_rect, 2, border_radius=self.border_radius)

        text_x = self.button_rect.x + (self.button_rect.width - self.image.get_width()) // 2
        text_y = self.button_rect.y + (self.button_rect.height - self.image.get_height()) // 2
        surface.blit(self.image, (text_x, text_y))

    def is_active(self):
        pos = pygame.mouse.get_pos()
        mouse_over = self.button_rect.collidepoint(pos)

        if mouse_over and pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            return True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return False


class BasicButton(Button):
    def __init__(self, x, y, text, width=300):
        super().__init__(
            x,
            y,
            text=text,
            font_size=30,
            text_color=colors.BUTTON_TEXT_COLOR,
            bg_color=colors.BUTTON_BACKGROUND_COLOR,
            hover_color=colors.BUTTON_HOVER_COLOR,
            width=width,
            height=50,
            padding=20,
            border_radius=10,
        )


class GoBackButton(Button):
    def __init__(self, x, y):
        super().__init__(
            x,
            y,
            text="Go back",
            font_size=22,
            text_color=colors.BUTTON_TEXT_COLOR,
            bg_color=colors.BUTTON_BACKGROUND_COLOR,
            hover_color=colors.BUTTON_HOVER_COLOR,
            width=100,
            height=30,
            padding=10,
            border_radius=10,
        )
