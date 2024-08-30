"""
Module for the battle end menu in the game. The `BattleEndMenu` class handles the end-of-battle screen,
displaying the results of the game and providing an option to exit the room.
"""

import pygame
from game.visuals.utils import colors
from game.visuals.utils.buttons import BasicButton
from game.menus.menu import Menu
from game.visuals.utils.draw_utils import DrawUtils


class BattleEndMenu(Menu):
    """
    Menu displayed at the end of a battle. Shows the results of the game, including whether the player won or lost,
    and provides an option to exit the room.
    """

    def __init__(self, menus_evolution, player, opponent_name):
        """
        Initialize the BattleEndMenu with player and opponent details, and set up the exit room button.

        Args:
            menus_evolution (list): List of menus in the evolution stack.
            player (Player): The player instance.
            opponent_name (str): The name of the opponent.
        """
        super().__init__(menus_evolution)

        self.player = player
        self.opponent_name = opponent_name

        self.exit_room_button = BasicButton(x=490, y=630, text="Exit room")
        self.ending_message = self.get_ending_message()
        print(self.ending_message)
        self.player.request_enemy_board()

    def draw(self, screen):
        """
        Draw the end-of-battle menu on the screen, including the player's board, the enemy's board view,
        the ending message, and the exit room button.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        super().draw(screen)

        self.player.board.draw(screen)
        self.player.enemy_board_view.draw(screen)
        DrawUtils.apply_color_overlay(screen, color=colors.TILE_MAIN_COLOR)

        DrawUtils.draw_popup_centered_message(
            screen,
            title_text=self.ending_message[0],
            subtitle_text=self.ending_message[1],
        )
        self.exit_room_button.draw(screen)

    def _get_winning_description(self):
        """
        Generate the description text for a winning result.

        Returns:
            str: A description of the victory outcome.
        """
        if self.player.is_timeout:
            return f"{self.opponent_name} was too afraid to make a move and left the battle!"

        return f"Congratulations {self.player.name}, you destroyed your opponent {self.opponent_name}!"

    def _get_losing_description(self):
        """
        Generate the description text for a losing result.

        Returns:
            str: A description of the defeat outcome.
        """
        if self.player.is_timeout:
            return f"{self.player.name}, you were paralyzed in fear and abandoned the battle like a coward!"

        return f"Better luck next time {self.player.name}, the win goes to {self.opponent_name}!"

    def get_ending_message(self):
        """
        Determine the appropriate ending message based on whether the player won or lost.

        Returns:
            tuple: A tuple containing the title and description of the ending message.
        """
        if self.player.is_winner:
            return (
                "You are victorious!",
                self._get_winning_description(),
            )

        return (
            "Defeat!",
            self._get_losing_description(),
        )

    def handle_event(self, event):
        """
        Handle user events such as button clicks. If the exit room button is clicked, transition to the first menu.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        super().handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.exit_room_button.is_active():
                first_menu_type = self.get_first_menu_in_evolution()
                self.next_menu = first_menu_type(self.player.name)
