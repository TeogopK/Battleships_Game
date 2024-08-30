"""
Module for handling the menu system in a game. The `Menu` class manages menu displays, message handling,
and menu evolution (navigating between different menus).
"""

import pygame

from game.visuals.utils.draw_utils import DrawUtils
from game.visuals.utils import colors


class Menu:
    """
    Class for representing and managing a menu in the game. Handles message display, menu evolution,
    and event handling for user interactions.
    """

    CLEAR_MESSAGE_EVENT = pygame.USEREVENT + 9
    MESSAGE_DISPLAY_TIME = 3000

    def __init__(
        self,
        menus_evolution=None,
        message_x=620,
        message_y=600,
    ):
        """
        Initialize the Menu with optional menu evolution history and message display coordinates.

        Args:
            menus_evolution (list, optional): A list tracking the evolution of menus. Defaults to an empty list.
            message_x (int): X-coordinate for message display. Defaults to 620.
            message_y (int): Y-coordinate for message display. Defaults to 600.
        """
        self.menus_evolution = menus_evolution if menus_evolution is not None else []

        self.message = ""
        self.message_x = message_x
        self.message_y = message_y
        self.next_menu = None

        self.add_self_to_evolution()

    def get_father_in_evolution(self):
        """
        Get the previous menu in the evolution history.

        Returns:
            Menu or None: The previous menu, or None if there are no more menus in the evolution history.
        """
        self.menus_evolution.pop()
        if not self.menus_evolution:
            return None
        return self.menus_evolution.pop()

    def add_self_to_evolution(self):
        """
        Add the current menu class to the evolution history.
        """
        self.menus_evolution.append(type(self))

    def get_first_menu_in_evolution(self):
        """
        Get the first menu in the evolution history.

        Returns:
            Menu: The first menu in the evolution history.
        """
        return self.menus_evolution[0]

    def handle_event(self, event):
        """
        Handle events, specifically clearing the displayed message when the custom clear message event is triggered.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == self.CLEAR_MESSAGE_EVENT:
            self.message = ""

    def draw(self, screen):
        """
        Draw the menu on the screen, including the background and any message.

        Args:
            screen (pygame.Surface): The screen to draw on.
        """
        screen.fill(colors.BACKGROUND_COLOR)

        if self.message:
            DrawUtils.draw_message(screen, self.message, x=self.message_x, y=self.message_y)

    def show_message(self, message):
        """
        Display a message on the screen and set a timer to clear it using a custom pygame event.

        Args:
            message (str): The message to display.
        """
        self.message = message
        pygame.time.set_timer(self.CLEAR_MESSAGE_EVENT, self.MESSAGE_DISPLAY_TIME)
