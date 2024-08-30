import pygame
from game.visuals.utils import constants

from game import menus


class Application:  # pylint: disable=R0903
    def __init__(
        self,
        width=constants.WINDOW_WIDTH,
        height=constants.WINDOW_HEIGHT,
        fps=constants.FPS,
    ):
        pygame.init()
        pygame.display.set_caption(constants.APPLICATION_TITLE)
        self.screen = pygame.display.set_mode((width, height))
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.menu = menus.StartMenu()

        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self._handle_events()
            self._draw_menu()

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.menu.handle_event(event)

            if self.menu.next_menu:
                self.menu = self.menu.next_menu

    def _draw_menu(self):
        self.menu.draw(self.screen)
        pygame.display.update()


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
