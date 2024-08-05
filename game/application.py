import pygame
from game.visuals.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, APPLICATION_TITLE
from game.menus.ship_placement_menu import ShipPlacementMenu

FPS = 60


class Application:
    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        pygame.init()
        pygame.display.set_caption(APPLICATION_TITLE)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ship_placement_menu = ShipPlacementMenu()

    def run(self):
        running = True

        while running:
            self.clock.tick(FPS)
            self.screen.fill((241, 250, 238))
            self.ship_placement_menu.draw(self.screen)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.ship_placement_menu.handle_event(event)

        pygame.quit()


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
