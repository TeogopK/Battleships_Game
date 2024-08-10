import pygame
import game.visuals.utils.constants as constants

from game.menus.ship_placement_menu import ShipPlacementMenu
from game.menus.battle_menu import BattleMenu
from game.menus.battle_end_menu import BattleEndMenu
from game.menus.start_menu import StartMenu

from game.players.player import Player
from game.players.ai_player import BattleAI
import game.visuals.utils.colors as colors


class Application:
    def __init__(self, width=constants.WINDOW_WIDTH, height=constants.WINDOW_HEIGHT, fps=constants.FPS):
        pygame.init()
        pygame.display.set_caption(constants.APPLICATION_TITLE)
        self.screen = pygame.display.set_mode((width, height))
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.menu = StartMenu()

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
