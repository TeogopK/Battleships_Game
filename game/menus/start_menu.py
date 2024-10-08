"""
Module for the start menu of the game. The `StartMenu` class handles player input, menu navigation,
and starting either an offline or multiplayer game.
"""

import pygame
from game.visuals.utils.buttons import BasicButton
from game.server.network import MultiplayerNetwork, OfflineNetwork
from game.server.game_server import SinglePlayerServer
from game.menus.menu import Menu
from game.players.player import Player
from game.visuals.utils.draw_utils import DrawUtils
from game.menus.ship_placement_menu import ShipPlacementMenu
from game.menus.multiplayer_menu import MultiplayerMenu


class StartMenu(Menu):
    """
    Start menu for the game. Provides options to start an offline game or a multiplayer game.
    Handles player input for entering a name and navigates to the appropriate menu based on user selection.
    """

    MAX_PLAYER_NAME_LENGTH = 10

    def __init__(self, name_input=""):
        """
        Initialize the StartMenu with buttons for offline and online play and an optional initial player name.

        Args:
            name_input (str): Initial input for the player's name. Defaults to an empty string.
        """
        super().__init__()
        self.play_offline_button = BasicButton(x=250, y=630, text="Play offline")
        self.play_online_button = BasicButton(x=650, y=630, text="Play online")
        self.name_input = name_input

    def handle_event(self, event):
        """
        Handle user events, including key presses and button interactions.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        super().handle_event(event)

        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)

        if self.play_offline_button.is_active():
            self.start_offline_game()

        if self.play_online_button.is_active():
            self.start_multiplayer_game()

    def handle_keydown(self, event):
        """
        Handle key press events for inputting player names.

        Args:
            event (pygame.event.Event): The key press event to handle.
        """
        allowed_name_keys = (
            set(range(pygame.K_a, pygame.K_z + 1)) | set(range(pygame.K_0, pygame.K_9 + 1)) | {pygame.K_MINUS}
        )

        if event.key == pygame.K_BACKSPACE:
            self.name_input = self.name_input[:-1]
        elif event.key in allowed_name_keys:
            if len(self.name_input) < self.MAX_PLAYER_NAME_LENGTH:
                self.name_input += event.unicode

    def get_player_name_input(self):
        """
        Get the player name input from the user.

        Returns:
            str: The player's name or "Player" if no name was entered.
        """
        return self.name_input if len(self.name_input) > 0 else "Player"

    def start_offline_game(self):
        """
        Start an offline game by setting up a SinglePlayerServer and a Player instance.
        Navigate to the ShipPlacementMenu for offline play.
        """
        offline_server = SinglePlayerServer()
        player = Player(self.get_player_name_input(), OfflineNetwork(is_player=True))

        player.network_client.add_server_instance(offline_server)

        room_id = offline_server.set_up_game_room(player)

        self.next_menu = ShipPlacementMenu(self.menus_evolution, player, room_id, offline_server.battle_bot.name)

    def start_multiplayer_game(self):
        """
        Start a multiplayer game by connecting to a MultiplayerNetwork instance.
        Navigate to the MultiplayerMenu for online play.
        """
        try:
            network_client = MultiplayerNetwork()
        except ConnectionError:
            self.show_message("Unable to connect to the server!")
            return

        self.next_menu = MultiplayerMenu(
            self.menus_evolution,
            network_client,
            self.get_player_name_input(),
        )

    def draw(self, screen):
        """
        Draw the start menu on the screen, including buttons, labels, and input text.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
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
