import pygame
import game.visuals.utils.constants as constants
from game.menus.ship_placement_menu import ShipPlacementMenu
from game.menus.battle_menu import BattleMenu
from game.menus.battle_end_menu import BattleEndMenu
from game.player import Player
import game.visuals.utils.colors as colors


class Application:
    def __init__(self, width=constants.WINDOW_WIDTH, height=constants.WINDOW_HEIGHT, fps=constants.FPS):
        pygame.init()
        pygame.display.set_caption(constants.APPLICATION_TITLE)
        self.screen = pygame.display.set_mode((width, height))
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.players = None
        self.ship_placement_menu = None
        self.battle_menu = None
        self.battle_end_menu = None
        self.in_placement_phase = True
        self.init_game()

    def init_game(self):
        """Initialize or reset the game."""
        self.players = [
            Player("Player 1", 70, 100),
            Player("Player 2", 700, 100)
        ]
        self.ship_placement_menu = ShipPlacementMenu(self.players[0])
        self.battle_menu = None
        self.battle_end_menu = None
        self.in_placement_phase = True

    def transition_to_battle(self):
        """Transition from the ship placement phase to the battle phase."""
        self.battle_menu = BattleMenu(self.players[0], self.players[1])
        self.in_placement_phase = False
        self.players[0].is_turn = True

    def transition_to_end_menu(self):
        """Transition to the battle end menu."""
        self.battle_end_menu = BattleEndMenu(self.players[0], self.players[1])

    def run(self):
        """Main application loop."""
        running = True
        while running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.in_placement_phase:
                    self.handle_ship_placement(event)
                elif self.battle_menu and self.battle_menu.stop_showing_menu:
                    self.transition_to_end_menu()
                    self.battle_menu = None
                elif self.battle_end_menu:
                    self.handle_end_menu(event)
                    if self.battle_end_menu.restart_game:
                        self.init_game()
                else:
                    self.handle_battle(event)

            self.update_screen()
            pygame.display.update()

        pygame.quit()

    def handle_ship_placement(self, event):
        """Handle events during the ship placement phase."""
        transition = self.ship_placement_menu.handle_event(event)
        if self.ship_placement_menu.stop_showing_menu:
            self.transition_to_battle()

    def handle_battle(self, event):
        """Handle events during the battle phase."""
        if self.battle_menu:
            self.battle_menu.handle_event(event)

    def handle_end_menu(self, event):
        """Handle events during the battle end phase."""
        if self.battle_end_menu:
            self.battle_end_menu.handle_event(event)

    def update_screen(self):
        """Update the screen based on the current phase."""
        if self.in_placement_phase:
            self.screen.fill(colors.BACKGROUND_COLOR)
            self.ship_placement_menu.draw(self.screen)
        elif self.battle_end_menu:
            self.battle_end_menu.draw(self.screen)
        elif self.battle_menu:
            self.battle_menu.draw(self.screen)


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
