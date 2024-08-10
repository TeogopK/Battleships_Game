import pygame
from game.visuals.utils.buttons import BasicButton
import game.visuals.utils.colors as colors
from game.menus.menu import Menu


class MultiplayerMenu(Menu):
    def __init__(self, client):
        super().__init__()
        self.client = client

        self.create_room_button = BasicButton(
            x=150, y=630, text="Create room", width=300)
        self.join_room_by_id_button = BasicButton(
            x=475, y=630, text="Join room by id", width=300)
        self.join_random_room_button = BasicButton(
            x=800, y=630, text="Join random room", width=300)

        self.next_menu = None

    def handle_event(self, event):
        if self.create_room_button.is_active():
            self.create_room()

        if self.join_room_by_id_button.is_active():
            self.join_room_by_id()

        if self.join_random_room_button.is_active():
            self.join_random_room()

    def create_room(self):
        self.client.send("create-room")

    def join_room_by_id(self):
        pass

    def join_random_room(self):
        pass

    def draw(self, screen):
        super().draw(screen)
        self.join_random_room_button.draw(screen)
        self.join_room_by_id_button.draw(screen)
        self.create_room_button.draw(screen)
