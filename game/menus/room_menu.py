import pygame
import json
from game.visuals.utils.buttons import BasicButton, GoBackButton
import game.menus as menus
from game.players.player import Player
from game.visuals.utils.shapes import DrawUtils
import game.visuals.utils.colors as colors

CHECK_OPPONENT_EVENT = pygame.USEREVENT + 1


class RoomMenu(menus.Menu):
    def __init__(self, player, room_id):
        super().__init__()
        self.player = player
        self.room_id = room_id
        self.exit_room_button = BasicButton(x=250, y=630, text="Exit room", width=300)
        self.change_publicity_button = BasicButton(
            x=650, y=630, text="Change publicity", width=300
        )

        self.next_menu = None
        self.is_room_private = False

        pygame.time.set_timer(CHECK_OPPONENT_EVENT, 2000)

    def handle_event(self, event):
        if self.exit_room_button.is_active():
            self.exit_room()

        if self.change_publicity_button.is_active():
            self.change_room_publicity()

        if event.type == CHECK_OPPONENT_EVENT:
            self.check_has_opponent_joined()

    def exit_room(self):
        response = self.player.exit_room()
        if response.get("status") == "success":
            self.next_menu = menus.MultiplayerMenu(
                self.player.network_client, self.player.name
            )

    def change_room_publicity(self):
        response = self.player.change_room_publicity()
        if response.get("status") == "success":
            self.is_room_private = response["args"]["is_private"]

    def get_room_privacy_label(self):
        return (
            "Private - Join with code only!"
            if self.is_room_private
            else "Public - Anyone can join!"
        )

    def check_has_opponent_joined(self):
        response = self.player.has_opponent_joined()
        if response.get("status") == "success":
            self.next_menu = menus.ShipPlacementMenu(self.player, self.room_id)

    def draw(self, screen):
        super().draw(screen)
        self.exit_room_button.draw(screen)
        self.change_publicity_button.draw(screen)

        DrawUtils.draw_title(screen, "Battleships", 620, 200, 128, glow_size=7)
        DrawUtils.draw_title(
            screen, f"Room ID: {self.room_id} ", 620, 300, 64, glow_size=3
        )

        DrawUtils.draw_label(screen, "Room privacy: ", x=620, y=450)
        DrawUtils.draw_input_text(screen, self.get_room_privacy_label(), x=620, y=500)
