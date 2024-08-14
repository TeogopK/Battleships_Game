import pygame
import json
from game.visuals.utils.buttons import BasicButton, GoBackButton
import game.menus as menus
from game.players.player import Player

CHECK_OPPONENT_EVENT = pygame.USEREVENT + 1


class WaitForOpponentMenu(menus.Menu):
    def __init__(self, player):
        super().__init__()
        self.player = player

        self.exit_room_button = BasicButton(
            x=475, y=630, text="Exit room", width=300)

        self.next_menu = None

        pygame.time.set_timer(CHECK_OPPONENT_EVENT, 2000)

    def handle_event(self, event):
        if self.exit_room_button.is_active():
            response = self.player.exit_room()
            if response.get('status') == 'success':
                pygame.time.set_timer(
                    CHECK_OPPONENT_EVENT, 0)
                self.next_menu = menus.MultiplayerMenu(
                    self.player.network_client)

        if event.type == CHECK_OPPONENT_EVENT:
            self.check_has_opponent_joined()

    def check_has_opponent_joined(self):
        response = self.player.has_opponent_joined()
        if response.get('status') == 'success':
            pygame.time.set_timer(CHECK_OPPONENT_EVENT, 0)
            self.next_menu = menus.ShipPlacementMenu(self.player)

    def draw(self, screen):
        super().draw(screen)
        self.exit_room_button.draw(screen)
