import pygame
import json
from game.visuals.utils.buttons import BasicButton, GoBackButton
import game.menus as menus
from game.menus.menu import Menu
from game.players.player import Player


class MultiplayerMenu(Menu):
    def __init__(self, client):
        super().__init__()
        self.player = Player("Player 1", client)

        self.create_room_button = BasicButton(x=150, y=630, text="Create room", width=300)
        self.join_room_with_id_button = BasicButton(x=475, y=630, text="Join room by id", width=300)
        self.join_random_room_button = BasicButton(x=800, y=630, text="Join random room", width=300)
        self.go_back_button = GoBackButton(10, 10)

        self.next_menu = None

    def handle_event(self, event):
        if self.create_room_button.is_active():
            response = self.player.create_room()
            self.handle_response(response, menus.WaitForOpponentMenu)

        if self.join_room_with_id_button.is_active():
            room_id = self.get_room_id()
            response = self.player.join_room_with_id(room_id)
            self.handle_response(response, menus.ShipPlacementMenu)

        if self.join_random_room_button.is_active():
            response = self.player.join_random_room()
            self.handle_response(response, menus.ShipPlacementMenu)

        if self.go_back_button.is_active():
            self.next_menu = menus.StartMenu()

    def handle_response(self, response, menu):
        if response.get("status") == "error":
            print(response.get("message", "Unknown error"))
            return

        print(response.get("message", "Operation successful"))
        self.next_menu = menu(self.player)

    def get_room_id(self):
        return "0"

    def draw(self, screen):
        super().draw(screen)
        self.create_room_button.draw(screen)
        self.join_room_with_id_button.draw(screen)
        self.join_random_room_button.draw(screen)
        self.go_back_button.draw(screen)
