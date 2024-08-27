import pygame
from game.visuals.utils.buttons import BasicButton
from game.server.network import MultiplayerNetwork, OfflineNetwork
from game.server.game_server import SinglePlayerServer
import game.menus as menus
import game.visuals.utils.colors as colors
from game.players.player import Player
from game.visuals.utils.draw_utils import DrawUtils


class StartMenu(menus.Menu):
    MAX_PLAYER_NAME_LENGTH = 20

    def __init__(self, name_input=""):
        super().__init__()
        self.play_offline_button = BasicButton(x=250, y=630, text="Play offline")
        self.play_online_button = BasicButton(x=650, y=630, text="Play online")
        self.name_input = name_input
        self.next_menu = None

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)

        if self.play_offline_button.is_active():
            self.start_offline_game()

        if self.play_online_button.is_active():
            self.start_multiplayer_game()

    def handle_keydown(self, event):
        allowed_name_keys = (
            set(range(pygame.K_a, pygame.K_z + 1))
            | set(range(pygame.K_0, pygame.K_9 + 1))
            | {pygame.K_MINUS}
        )

        if event.key == pygame.K_BACKSPACE:
            self.name_input = self.name_input[:-1]
        elif event.key in allowed_name_keys:
            if len(self.name_input) < self.MAX_PLAYER_NAME_LENGTH:
                self.name_input += event.unicode

    def get_player_name_input(self):
        return self.name_input if len(self.name_input) > 0 else "Player"

    def start_offline_game(self):
        offline_server = SinglePlayerServer()
        player = Player(self.get_player_name_input(), OfflineNetwork(is_player=True))

        player.network_client.add_server_instance(offline_server)

        room_id = offline_server.set_up_game_room(player)

        self.next_menu = menus.ShipPlacementMenu(
            player, room_id, offline_server.battle_bot.name
        )

    def start_multiplayer_game(self):
        try:
            network_client = MultiplayerNetwork()
        except ConnectionError:
            print("SErver")
            self.show_message("Unable to connect to the server!")
            return

        self.next_menu = menus.MultiplayerMenu(
            network_client, self.get_player_name_input()
        )

    def draw(self, screen):
        super().draw(screen)

        self.play_online_button.draw(screen)
        self.play_offline_button.draw(screen)
        DrawUtils.draw_label(screen, "Enter your battle name:", x=620, y=450)
        DrawUtils.draw_input_text(
            screen,
            self.get_player_name_input(),
            x=620,
            y=500,
        )
        DrawUtils.draw_title(screen, "Battleships", 620, 200, 128, glow_size=7)
