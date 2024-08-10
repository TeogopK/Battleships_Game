import pygame
from game.visuals.utils.buttons import BasicButton
from game.server.network import Network
from game.menus.ship_placement_menu import ShipPlacementMenu
from game.menus.multiplayer_menu import MultiplayerMenu
from game.menus.menu import Menu
import game.visuals.utils.colors as colors
from game.players.player import Player


class StartMenu(Menu):
    def __init__(self):
        super().__init__()
        self.play_offline_button = BasicButton(
            x=250, y=630, text="Play offline")
        self.play_online_button = BasicButton(x=650, y=630, text="Play online")
        self.next_menu = None

    def handle_event(self, event):
        if self.play_offline_button.is_active():
            self.start_offline_game()

        if self.play_online_button.is_active():
            self.start_multiplayer_game()

    def start_offline_game(self):
        player = Player("Player 1", 70, 100)
        self.next_menu = ShipPlacementMenu(player)

    def start_multiplayer_game(self):
        try:
            network_client = Network()
        except ConnectionError:
            print("Connection error!")

        self.next_menu = MultiplayerMenu(network_client)

    def draw(self, screen):
        super().draw(screen)
        self.play_online_button.draw(screen)
        self.play_offline_button.draw(screen)
