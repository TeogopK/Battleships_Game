import pygame
import json
from game.visuals.utils.buttons import BasicButton, GoBackButton
import game.menus as menus
from game.menus.menu import Menu
from game.players.player import Player
from game.visuals.utils.shapes import DrawUtils
import game.visuals.utils.colors as colors

CLEAR_MESSAGE_EVENT = pygame.USEREVENT + 9


class MultiplayerMenu(Menu):
    GAME_ROOM_ID_LENGTH = 6
    MESSAGE_DISPLAY_TIME = 3000

    def __init__(self, client, player_name):
        super().__init__()
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

        self.next_menu = None
        self.room_id_input = ""
        self.message = ""

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)

        if event.type == CLEAR_MESSAGE_EVENT:
            self.message = ""

        if self.create_room_button.is_active():
            response = self.player.create_room()
            self.handle_response(response, menus.RoomMenu)

        if self.join_room_with_id_button.is_active():
            self.process_join_room_by_id()

        if self.join_random_room_button.is_active():
            response = self.player.join_random_room()
            self.handle_response(response, menus.ShipPlacementMenu)

        if self.go_back_button.is_active():
            self.next_menu = menus.StartMenu(self.player.name)

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
        self.handle_response(response, menus.ShipPlacementMenu)

    def handle_response(self, response, menu):
        if response.get("status") == "error":
            self.show_message(response["message"])
            return

        room_id = response["args"]["room_id"]
        self.next_menu = menu(self.player, room_id)

    def show_message(self, message):
        """Displays a message and sets a timer to clear it using a custom pygame event."""
        self.message = message
        pygame.time.set_timer(CLEAR_MESSAGE_EVENT, self.MESSAGE_DISPLAY_TIME)

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

        if self.message:
            DrawUtils.draw_message(screen, self.message, x=620, y=600)
