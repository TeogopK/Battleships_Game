import pygame
from game.visuals.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, APPLICATION_TITLE
from game.menus.ship_placement_menu import ShipPlacementMenu
from game.menus.battle_menu import BattleMenu
from game.player import Player

FPS = 60


class Application:
    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        pygame.init()
        pygame.display.set_caption(APPLICATION_TITLE)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.players = [
            Player("Player 1", 10, 40),
            Player("Player 2", 600, 40)
        ]
        self.ship_placement_menu = ShipPlacementMenu(self.players[0])
        self.battle_menu = None
        self.in_placement_phase = True

    def transition_to_battle(self):
        """Transition from the ship placement phase to the battle phase."""
        self.battle_menu = BattleMenu(self.players[0], self.players[1])
        self.in_placement_phase = False
        self.players[0].is_turn = True

    def run(self):
        """Main application loop."""
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.in_placement_phase:
                    self.handle_ship_placement(event)
                else:
                    self.handle_battle(event)

            self.update_screen()
            pygame.display.update()

        pygame.quit()

    def handle_ship_placement(self, event):
        """Handle events during the ship placement phase."""
        transition = self.ship_placement_menu.handle_event(event)
        if self.ship_placement_menu.finish_phase:
            self.transition_to_battle()

    def handle_battle(self, event):
        """Handle events during the battle phase."""
        self.battle_menu.handle_event(event)

    def update_screen(self):
        """Update the screen based on the current phase."""
        if self.in_placement_phase:
            self.screen.fill((241, 250, 238))
            self.ship_placement_menu.draw(self.screen)
        else:
            self.battle_menu.draw(self.screen)
            if self.battle_menu.check_game_over():
                print("Game Over")
                pygame.quit()


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
