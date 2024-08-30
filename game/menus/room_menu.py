"""
Module for the room menu in the game. The `RoomMenu` class handles actions related to room management
such as exiting a room, changing room publicity, and waiting for an opponent to join.
"""

import pygame
from game.visuals.utils.buttons import BasicButton
from game.menus.menu import Menu
from game.visuals.utils.draw_utils import DrawUtils
from game.menus.ship_placement_menu import ShipPlacementMenu


class RoomMenu(Menu):
    """
    Room menu that allows the player to exit the room, change room publicity, and checks for an opponent joining.
    Handles drawing the room information and waiting messages.
    """

    CHECK_OPPONENT_EVENT = pygame.USEREVENT + 3
    UPDATE_WAITING_MESSAGE_EVENT = pygame.USEREVENT + 4

    def __init__(self, menus_evolution, player, room_id):
        """
        Initialize the RoomMenu with buttons for room management and sets up timers for checking opponent status.

        Args:
            menus_evolution (list): List of menus in the evolution stack.
            player (Player): The player instance managing room actions.
            room_id (str): The ID of the current room.
        """
        super().__init__(menus_evolution)
        self.player = player
        self.room_id = room_id
        self.exit_room_button = BasicButton(x=250, y=630, text="Exit room", width=300)
        self.change_publicity_button = BasicButton(x=650, y=630, text="Change publicity", width=300)

        self.is_room_private = False

        pygame.time.set_timer(self.CHECK_OPPONENT_EVENT, 2000)
        pygame.time.set_timer(self.UPDATE_WAITING_MESSAGE_EVENT, 500)

        self.waiting_dots = 0

    def handle_event(self, event):
        """
        Handle user events including button clicks and custom events.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        super().handle_event(event)

        if self.exit_room_button.is_active():
            self.exit_room()

        if self.change_publicity_button.is_active():
            self.change_room_publicity()

        if event.type == self.CHECK_OPPONENT_EVENT:
            self.check_has_opponent_joined()

        if event.type == self.UPDATE_WAITING_MESSAGE_EVENT:
            self.update_waiting_dots()

    def exit_room(self):
        """
        Handle exiting the room. Navigates back to the previous menu if successful.
        """
        response = self.player.exit_room()
        if response.get("status") == "success":
            previous_menu_type = self.get_father_in_evolution()
            self.next_menu = previous_menu_type(self.menus_evolution, self.player.network_client, self.player.name)

    def change_room_publicity(self):
        """
        Handle changing the room's publicity status between private and public.
        """
        response = self.player.change_room_publicity()
        if response.get("status") == "success":
            self.is_room_private = response["args"]["is_private"]

    def get_room_privacy_label(self):
        """
        Get the label indicating the room's privacy status.

        Returns:
            str: The privacy status label.
        """
        return "Private - Join with code only!" if self.is_room_private else "Public - Anyone can join!"

    def check_has_opponent_joined(self):
        """
        Check if an opponent has joined the room. Navigates to ShipPlacementMenu if an opponent has joined.
        """
        response = self.player.has_opponent_joined()
        if response.get("status") == "success":
            opponent_name = response["args"]["opponent_name"]
            self.next_menu = ShipPlacementMenu(self.menus_evolution, self.player, self.room_id, opponent_name)

    def update_waiting_dots(self):
        """
        Update the waiting message dots to indicate the waiting status.
        """
        self.waiting_dots = (self.waiting_dots + 1) % 4

    def get_waiting_message(self):
        """
        Get the message indicating that the player is waiting for an opponent to join.

        Returns:
            str: The waiting message with dynamic dots.
        """
        return f"Waiting for someone to join{'.' * self.waiting_dots}"

    def draw(self, screen):
        """
        Draw the room menu on the screen, including buttons, labels, and waiting messages.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        super().draw(screen)
        self.exit_room_button.draw(screen)
        self.change_publicity_button.draw(screen)

        DrawUtils.draw_title(screen, "Battleships", 620, 200, 128, glow_size=7)
        DrawUtils.draw_title(screen, f"Room ID: {self.room_id} ", 620, 300, 64, glow_size=3)

        DrawUtils.draw_label(screen, "Room privacy: ", x=620, y=430)
        DrawUtils.draw_input_text(screen, self.get_room_privacy_label(), x=620, y=480)

        DrawUtils.draw_label(screen, self.get_waiting_message(), x=620, y=570)
