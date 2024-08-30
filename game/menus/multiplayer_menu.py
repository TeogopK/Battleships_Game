import pygame
from game.visuals.utils.buttons import BasicButton, GoBackButton
from game.menus.menu import Menu
from game.players.player import Player
from game.visuals.utils.draw_utils import DrawUtils
from game.menus.ship_placement_menu import ShipPlacementMenu
from game.menus.room_menu import RoomMenu


class MultiplayerMenu(Menu):
    GAME_ROOM_ID_LENGTH = 6

    def __init__(self, menus_evolution, client, player_name):
        super().__init__(menus_evolution)
        self.player = Player(player_name, client)

        self.create_room_button = BasicButton(
            x=150, y=630, text="Create room", width=300
        )
        self.join_room_with_id_button = BasicButton(
            x=475, y=630, text="Join room by id", width=300
        )
        self.join_random_room_button = BasicButton(
            x=800, y=630, text="Join random room", width=300
        )
        self.go_back_button = GoBackButton(10, 10)

        self.room_id_input = ""

    def handle_event(self, event):
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
        if event.key == pygame.K_BACKSPACE:
            self.room_id_input = self.room_id_input[:-1]
        elif event.key == pygame.K_RETURN:
            self.process_join_room_by_id()
        elif event.key in range(pygame.K_0, pygame.K_9 + 1):
            if len(self.room_id_input) < self.GAME_ROOM_ID_LENGTH:
                self.room_id_input += str(event.key - pygame.K_0)

    def process_join_room_by_id(self):
        if len(self.room_id_input) != self.GAME_ROOM_ID_LENGTH:
            self.show_message("Enter a valid Room ID using the keyboard!")
            return

        room_id = self.room_id_input
        response = self.player.join_room_with_id(room_id)
        self.handle_join_room_response(response)

    def handle_create_room_response(self, response):
        """Handles the response for creating a room."""
        if response.get("status") == "error":
            self.show_message(response["message"])
            return

        room_id = response["args"]["room_id"]
        self.next_menu = RoomMenu(self.menus_evolution, self.player, room_id)

    def handle_join_room_response(self, response):
        """Handles the response for joining a room (either by ID or random)."""
        if response.get("status") == "error":
            self.show_message(response["message"])
            return

        room_id = response["args"]["room_id"]
        opponent_name = response["args"]["opponent_name"]
        self.next_menu = ShipPlacementMenu(
            self.menus_evolution, self.player, room_id, opponent_name
        )

    def get_input_text(self):
        return self.room_id_input + "-" * (
            self.GAME_ROOM_ID_LENGTH - len(self.room_id_input)
        )

    def draw(self, screen):
        super().draw(screen)
        self.create_room_button.draw(screen)
        self.join_room_with_id_button.draw(screen)
        self.join_random_room_button.draw(screen)
        self.go_back_button.draw(screen)

        DrawUtils.draw_title(screen, "Battleships", 620, 200, 128, glow_size=7)
        DrawUtils.draw_title(screen, "Multiplayer", 620, 300, 64, glow_size=3)

        DrawUtils.draw_label(
            screen, "Enter 6-digit Room ID to join a specific room:", x=620, y=450
        )
        DrawUtils.draw_input_text(screen, self.get_input_text(), x=620, y=500)
