import pygame

from game.visuals.utils.draw_utils import DrawUtils
import game.visuals.utils.colors as colors


class Menu:
    CLEAR_MESSAGE_EVENT = pygame.USEREVENT + 9
    MESSAGE_DISPLAY_TIME = 3000

    def __init__(self, message_x=620, message_y=600):
        self.next_menu = None

        self.message = ""
        self.message_x = message_x
        self.message_y = message_y

    def handle_event(self, event):
        if event.type == self.CLEAR_MESSAGE_EVENT:
            self.message = ""

    def draw(self, screen):
        screen.fill(colors.BACKGROUND_COLOR)

        if self.message:
            DrawUtils.draw_message(
                screen, self.message, x=self.message_x, y=self.message_y
            )

    def show_message(self, message):
        """Displays a message and sets a timer to clear it using a custom pygame event."""
        self.message = message
        pygame.time.set_timer(self.CLEAR_MESSAGE_EVENT, self.MESSAGE_DISPLAY_TIME)
