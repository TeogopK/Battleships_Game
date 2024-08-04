from game.visuals.utils.colours import WHITE, BLUE, BLACK, LIGHT_BLUE
import pygame
import pygame.freetype


class Button:
    def __init__(self, x, y, text, font_size, text_color, bg_color, hover_color, padding=10, border_radius=5):
        self.font = pygame.freetype.SysFont('Arial', font_size)
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.padding = padding
        self.border_radius = border_radius
        self.clicked = False

        # Create text surface
        self.image, self.rect = self.create_text_surface(text, text_color)
        self.rect.topleft = (x, y)
        self.update_rect_size()

    def create_text_surface(self, text, color):
        text_surface, rect = self.font.render(text, color)
        return text_surface, rect

    def update_rect_size(self):
        text_width, text_height = self.image.get_size()
        self.rect.width = text_width + 2 * self.padding
        self.rect.height = text_height + 2 * self.padding

    def is_active(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        mouse_over = self.rect.collidepoint(pos)

        # Draw button background with rounded corners
        bg_color = self.hover_color if mouse_over else self.bg_color
        pygame.draw.rect(surface, bg_color, self.rect,
                         border_radius=self.border_radius)

        # Center the text
        text_x = self.rect.x + self.padding
        text_y = self.rect.y + self.padding
        surface.blit(self.image, (text_x, text_y))

        # Check for click
        if mouse_over and pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
            self.clicked = True
            action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action


class ShuffleButton(Button):
    def __init__(self, x, y):
        # Define specific parameters for ShuffleButton
        super().__init__(x, y, text="Shuffle", font_size=30, text_color=WHITE,
                         bg_color=BLUE, hover_color=LIGHT_BLUE, padding=20, border_radius=10)
