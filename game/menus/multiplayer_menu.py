"""
Module for the multiplayer menu in the game. The `MultiplayerMenu` class handles creating a room,
joining a room by ID or randomly, and navigating to the appropriate next menu based on user actions.
"""

import pygame
from game.visuals.utils.buttons import BasicButton, GoBackButton
from game.menus.menu import Menu
from game.players.player import Player
from game.visuals.utils.draw_utils import DrawUtils
from game.menus.ship_placement_menu import ShipPlacementMenu
from game.menus.room_menu import RoomMenu


class MultiplayerMenu(Menu):
    """
    Multiplayer menu that allows the player to create a new game room, join an existing room by ID,
    or join a random room. Also handles navigation to the appropriate menu based on user actions.
    """

    GAME_ROOM_ID_LENGTH = 6

    def __init__(self, menus_evolution, client, player_name):
        """
        Initialize the MultiplayerMenu with buttons for room management and a player instance.

        Args:
            menus_evolution (list): List of menus in the evolution stack.
            client (network.Client): The network client for multiplayer interactions.
            player_name (str): The name of the player.
        """
        super().__init__(menus_evolution)
        self.player = Player(player_name, client)

        self.create_room_button = BasicButton(x=150, y=630, text="Create room", width=300)
        self.join_room_with_id_button = BasicButton(x=475, y=630, text="Join room by id", width=300)
        self.join_random_room_button = BasicButton(x=800, y=630, text="Join random room", width=300)
        self.go_back_button = GoBackButton(10, 10)

        self.room_id_input = ""

    def handle_event(self, event):
        """
        Handle user events including key presses and button clicks.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        super().handle_event(event)

        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)

        if self.create_room_button.is_active():
            response = self.player.create_room()
            self.handle_create_room_response(response)

        if self.join_room_with_id_button.is_active():
            self.process_join_room_by_id()

        if self.join_random_room_button.is_active():
            response = self.player.join_random_room()
            self.handle_join_room_response(response)

        if self.go_back_button.is_active():
            previous_menu_type = self.get_father_in_evolution()
            self.next_menu = previous_menu_type(self.player.name)

    def handle_keydown(self, event):
        """
        Handle key press events for inputting a room ID.

        Args:
            event (pygame.event.Event): The key press event to handle.
        """
        if event.key == pygame.K_BACKSPACE:
            self.room_id_input = self.room_id_input[:-1]
        elif event.key == pygame.K_RETURN:
            self.process_join_room_by_id()
        elif event.key in range(pygame.K_0, pygame.K_9 + 1):
            if len(self.room_id_input) < self.GAME_ROOM_ID_LENGTH:
                self.room_id_input += str(event.key - pygame.K_0)

    def process_join_room_by_id(self):
        """
        Process joining a room by ID, validating the room ID length and sending the join request.
        """
        if len(self.room_id_input) != self.GAME_ROOM_ID_LENGTH:
            self.show_message("Enter a valid Room ID using the keyboard!")
            return

        room_id = self.room_id_input
        response = self.player.join_room_with_id(room_id)
        self.handle_join_room_response(response)

    def handle_create_room_response(self, response):
        """
        Handle the response for creating a room. Navigate to the RoomMenu if successful.

        Args:
            response (dict): The response from the server after attempting to create a room.
        """
        if response.get("status") == "error":
            self.show_message(response["message"])
            return

        room_id = response["args"]["room_id"]
        self.next_menu = RoomMenu(self.menus_evolution, self.player, room_id)

    def handle_join_room_response(self, response):
        """
        Handle the response for joining a room (by ID or randomly). Navigate to ShipPlacementMenu if successful.

        Args:
            response (dict): The response from the server after attempting to join a room.
        """
        if response.get("status") == "error":
            self.show_message(response["message"])
            return

        room_id = response["args"]["room_id"]
        opponent_name = response["args"]["opponent_name"]
        self.next_menu = ShipPlacementMenu(self.menus_evolution, self.player, room_id, opponent_name)

    def get_input_text(self):
        """
        Get the formatted room ID input text for display.

        Returns:
            str: The room ID input text, padded with hyphens if necessary.
        """
        return self.room_id_input + "-" * (self.GAME_ROOM_ID_LENGTH - len(self.room_id_input))

    def draw(self, screen):
        """
        Draw the multiplayer menu on the screen, including buttons, labels, and input text.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        super().draw(screen)
        self.create_room_button.draw(screen)
        self.join_room_with_id_button.draw(screen)
        self.join_random_room_button.draw(screen)
        self.go_back_button.draw(screen)

        DrawUtils.draw_title(screen, "Battleships", 620, 200, 128, glow_size=7)
        DrawUtils.draw_title(screen, "Multiplayer", 620, 300, 64, glow_size=3)

        DrawUtils.draw_label(screen, "Enter 6-digit Room ID to join a specific room:", x=620, y=450)
        DrawUtils.draw_input_text(screen, self.get_input_text(), x=620, y=500)
