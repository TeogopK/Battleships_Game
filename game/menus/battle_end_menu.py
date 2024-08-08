import pygame
import game.visuals.utils.colors as colors
from game.visuals.utils.buttons import Button, ContinueButton


class BattleEndMenu:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.continue_button = ContinueButton(
            x=550, y=630)
        self.restart_game = False

    def draw(self, screen):
        self.player.board.draw(screen)
        self.enemy.board.draw(screen)
        self.continue_button.draw(screen)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.continue_button.is_active():
                self.restart_game = True
