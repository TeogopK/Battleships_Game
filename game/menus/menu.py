from abc import ABC, abstractmethod
import game.visuals.utils.colors as colors


class Menu(ABC):
    def __init__(self):
        self.next_menu = None

    @abstractmethod
    def handle_event(self, event):
        pass

    def draw(self, screen):
        screen.fill(colors.BACKGROUND_COLOR)
