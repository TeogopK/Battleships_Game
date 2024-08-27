import pygame
import game.visuals.utils.constants as constants

import game.menus as menus


class Application:
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

    def run(self):
        running = True
        while running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.menu.handle_event(event)

                if self.menu.next_menu:
                    self.menu = self.menu.next_menu

            self.menu.draw(self.screen)
            pygame.display.update()

        pygame.quit()


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
