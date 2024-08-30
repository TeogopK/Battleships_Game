"""
Module for the battle phase menu in the game. The `BattleMenu` class manages the game's battle phase, including
handling player and opponent turns, drawing game boards, and managing the hover and click interactions.
"""

import time
import pygame
from game.menus.menu import Menu
from game.visuals.utils.draw_utils import DrawUtils
from game.menus.battle_end_menu import BattleEndMenu


class BattleMenu(Menu):
    """
    Battle menu for the battle phase of the game. Handles displaying game boards, managing player turns, and
    updating the battle status.
    """

    ASK_RECEIVE_SHOT_EVENT = pygame.USEREVENT + 5

    def __init__(self, menus_evolution, player, opponent_name):
        """
        Initialize the BattleMenu with player and opponent details, and set up the event timers.

        Args:
            menus_evolution (list): List of menus in the evolution stack.
            player (Player): The player instance participating in the battle.
            opponent_name (str): The name of the opponent.
        """
        super().__init__(menus_evolution, message_x=137, message_y=690)
        self.player = player
        self.opponent_name = opponent_name

        pygame.time.set_timer(self.ASK_RECEIVE_SHOT_EVENT, 1000)

        self.last_hovered_tile = None
        self.is_battle_over = False

    def draw(self, screen):
        """
        Draw the battle menu on the screen, including the game boards, titles, and timers.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        super().draw(screen)
        self.player.board.draw(screen)
        self.player.enemy_board_view.draw(screen)

        DrawUtils.draw_title(screen, "Battle phase", x=635, y=40, font_size=60, glow_size=3)

        DrawUtils.draw_title(screen, self.player.name, x=110, y=650, font_size=42, glow_size=3)
        DrawUtils.draw_title(screen, self.opponent_name, x=768, y=650, font_size=42, glow_size=3)
        DrawUtils.draw_label(screen, text="Turn ends in:", x=430, y=650)
        DrawUtils.draw_label(screen, text="Turn ends in:", x=1050, y=650)

        self.draw_timer_based_on_turn(screen)

    def draw_timer_based_on_turn(self, screen):
        """
        Draw the timer showing the remaining time for the current turn.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        time_left = str(self.get_time_till_turn_end())
        time_left_opponent = time_left_player = "-"

        if self.player.is_turn:
            time_left_player = time_left
            turn_arrow = ">"
        else:
            time_left_opponent = time_left
            turn_arrow = "<"

        DrawUtils.draw_label(screen, text=turn_arrow, x=625, y=350, font_size=90)
        DrawUtils.draw_input_text(screen, text=time_left_player, x=540, y=650)
        DrawUtils.draw_input_text(screen, text=time_left_opponent, x=1160, y=650)

    def get_time_till_turn_end(self):
        """
        Calculate the remaining time until the turn ends.

        Returns:
            int: The number of seconds left until the turn ends, or 0 if time is up.
        """
        left_time = int(self.player.turn_end_time - time.time())
        return left_time if left_time >= 0 else 0

    def handle_event(self, event):
        """
        Handle user events such as mouse movements and clicks.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        super().handle_event(event)

        if self.is_battle_over:
            self.next_menu = BattleEndMenu(self.menus_evolution, self.player, self.opponent_name)
            return

        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            self.update_hovered_tile(pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if not self.player.is_turn:
                self.show_message("Wait for your turn!")

            elif self.is_click_within_enemy_board(pos):
                self.clear_hovered_tile()
                self.send_shot_command(pos)

        if event.type == self.ASK_RECEIVE_SHOT_EVENT:
            if not self.player.is_turn:
                self.ask_for_shot_command()

        self.is_battle_over = self.player.is_in_finished_battle

    def is_click_within_enemy_board(self, pos):
        """
        Check if the mouse click is within the enemy's board area.

        Args:
            pos (tuple): The mouse position.

        Returns:
            bool: True if the click is within the enemy board, False otherwise.
        """
        return self.player.enemy_board_view.is_position_in_board(pos)

    def ask_for_shot_command(self):
        """
        Request the player to receive a shot from the opponent.
        """
        self.player.ask_to_receive_shot()

    def send_shot_command(self, pos):
        """
        Send a shot command to the opponent based on the clicked position.

        Args:
            pos (tuple): The mouse position where the shot is aimed.
        """
        row, col = self.player.enemy_board_view.get_row_col_by_mouse(pos)

        if self.player.enemy_board_view.is_coordinate_shot_at(row, col):
            return

        self.player.shot(row, col)

        self.is_battle_over = self.player.is_in_finished_battle

    def update_hovered_tile(self, mouse_pos):
        """
        Update the tile that is currently hovered by the mouse.

        Args:
            mouse_pos (tuple): The current position of the mouse.
        """
        row, col = self.player.enemy_board_view.get_row_col_by_mouse(mouse_pos)

        if not self.player.enemy_board_view.is_coordinate_in_board(row, col):
            self.clear_hovered_tile()
            return

        if self.player.enemy_board_view.is_coordinate_shot_at(row, col):
            self.clear_hovered_tile()
        else:
            self.set_hovered_tile(row, col)

    def set_hovered_tile(self, row, col):
        """
        Set the current tile as hovered and clear the previous one if necessary.

        Args:
            row (int): The row of the tile.
            col (int): The column of the tile.
        """
        new_hovered_tile = self.player.enemy_board_view.tiles[row][col]

        if self.last_hovered_tile is not None and self.last_hovered_tile != new_hovered_tile:
            self.last_hovered_tile.set_hover(False)

        new_hovered_tile.set_hover(True)
        self.last_hovered_tile = new_hovered_tile

    def clear_hovered_tile(self):
        """
        Clear the hover state of the last hovered tile.
        """
        if self.last_hovered_tile is not None:
            self.last_hovered_tile.set_hover(False)
            self.last_hovered_tile = None
