import pygame
import json
import time
import game.menus as menus
from game.visuals.visual_board import VisualBoard


class BattleMenu(menus.Menu):
    ASK_RECEIVE_SHOT_EVENT = pygame.USEREVENT + 5

    def __init__(self, player, opponent_name):
        super().__init__(message_x=620, message_y=650)
        self.player = player
        self.opponent_name = opponent_name

        pygame.time.set_timer(self.ASK_RECEIVE_SHOT_EVENT, 1000)

        self.last_hovered_tile = None
        self.is_battle_over = False

    def draw(self, screen):
        super().draw(screen)
        self.player.board.draw(screen)
        self.player.enemy_board_view.draw(screen)

    def handle_event(self, event):
        super().handle_event(event)

        if self.is_battle_over:
            self.next_menu = menus.BattleEndMenu(self.player, self.opponent_name)
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
        return self.player.enemy_board_view.is_position_in_board(pos)

    def ask_for_shot_command(self):
        self.player.ask_to_receive_shot()

    def send_shot_command(self, pos):
        row, col = self.player.enemy_board_view.get_row_col_by_mouse(pos)

        if self.player.enemy_board_view.is_coordinate_shot_at(row, col):
            return

        self.player.shot(row, col)

        self.is_battle_over = self.player.is_in_finished_battle

    def update_hovered_tile(self, mouse_pos):
        """Update the tile that is currently hovered by the mouse."""
        row, col = self.player.enemy_board_view.get_row_col_by_mouse(mouse_pos)

        if not self.player.enemy_board_view.is_coordinate_in_board(row, col):
            self.clear_hovered_tile()
            return

        if self.player.enemy_board_view.is_coordinate_shot_at(row, col):
            self.clear_hovered_tile()
        else:
            self.set_hovered_tile(row, col)

    def set_hovered_tile(self, row, col):
        """Set the current tile as hovered and clear the previous one if necessary."""
        new_hovered_tile = self.player.enemy_board_view.tiles[row][col]

        if (
            self.last_hovered_tile is not None
            and self.last_hovered_tile != new_hovered_tile
        ):
            self.last_hovered_tile.set_hover(False)

        new_hovered_tile.set_hover(True)
        self.last_hovered_tile = new_hovered_tile

    def clear_hovered_tile(self):
        """Clear the hover state of the last hovered tile."""
        if self.last_hovered_tile is not None:
            self.last_hovered_tile.set_hover(False)
            self.last_hovered_tile = None
