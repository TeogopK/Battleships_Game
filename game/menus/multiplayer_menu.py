import pygame
import json
from game.visuals.utils.buttons import BasicButton, GoBackButton
import game.menus as menus
from game.menus.menu import Menu
from game.players.player import Player
from game.visuals.utils.shapes import DrawUtils
import game.visuals.utils.colors as colors


class MultiplayerMenu(Menu):
    def __init__(self, client):
        super().__init__()
        self.player = Player("Player 1", client)

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
        self.current_input = ""

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)

        if self.create_room_button.is_active():
            response = self.player.create_room()
            self.handle_response(response, menus.WaitForOpponentMenu)

        if self.join_room_with_id_button.is_active():
            self.process_join_room_by_id()

        if self.join_random_room_button.is_active():
            response = self.player.join_random_room()
            self.handle_response(response, menus.ShipPlacementMenu)

        if self.go_back_button.is_active():
            self.next_menu = menus.StartMenu()

    def handle_keydown(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.current_input = self.current_input[:-1]
        elif event.key == pygame.K_RETURN:
            self.process_join_room_by_id()
        elif event.key in range(pygame.K_0, pygame.K_9 + 1):
            if len(self.current_input) < 6:
                self.current_input += str(event.key - pygame.K_0)

    def process_join_room_by_id(self):
        if len(self.current_input) == 6:
            room_id = self.current_input
            response = self.player.join_room_with_id(room_id)
            self.handle_response(response, menus.ShipPlacementMenu)

    def handle_response(self, response, menu):
        if response.get("status") == "error":
            print(response.get("message", "Unknown error"))
            return

        print(response.get("message", "Operation successful"))
        self.next_menu = menu(self.player)

    def draw_input_text(self, screen):
        input_text = self.current_input + "-" * (6 - len(self.current_input))
        input_font = pygame.font.Font(None, 48)
        input_surface = input_font.render(input_text, True, colors.TEXT_LABEL_COLOR)
        input_rect = input_surface.get_rect(center=(620, 500))
        screen.blit(input_surface, input_rect)

    def draw_label(self, screen):
        font = pygame.font.Font(None, 24)
        explanation_surface = font.render(
            "Enter 6-digit Room ID to join a specific room:",
            True,
            colors.TEXT_LABEL_COLOR,
        )
        explanation_rect = explanation_surface.get_rect(center=(620, 450))
        screen.blit(explanation_surface, explanation_rect)

    def draw(self, screen):
        super().draw(screen)
        self.create_room_button.draw(screen)
        self.join_room_with_id_button.draw(screen)
        self.join_random_room_button.draw(screen)
        self.go_back_button.draw(screen)

        DrawUtils.draw_title(screen, "Battleships", 128, 620, 200, glow_size=7)
        DrawUtils.draw_title(screen, "Multiplayer", 64, 620, 300, glow_size=3)

        self.draw_input_text(screen)
        self.draw_label(screen)
