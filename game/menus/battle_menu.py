import pygame
import json
import time
import game.menus as menus
from game.visuals.visual_board import VisualBoard
from game.visuals.utils.draw_utils import DrawUtils


class BattleMenu(menus.Menu):
    ASK_RECEIVE_SHOT_EVENT = pygame.USEREVENT + 5

    def __init__(self, player, opponent_name):
        super().__init__(message_x=137, message_y=690)
        self.player = player
        self.opponent_name = opponent_name

        pygame.time.set_timer(self.ASK_RECEIVE_SHOT_EVENT, 1000)

        self.last_hovered_tile = None
        self.is_battle_over = False

    def draw(self, screen):
        super().draw(screen)
        self.player.board.draw(screen)
        self.player.enemy_board_view.draw(screen)

        DrawUtils.draw_title(
            screen, "Battle phase", x=635, y=40, font_size=60, glow_size=3
        )

        DrawUtils.draw_title(
            screen, self.player.name, x=110, y=650, font_size=42, glow_size=3
        )
        DrawUtils.draw_title(
            screen, self.opponent_name, x=768, y=650, font_size=42, glow_size=3
        )
        DrawUtils.draw_label(screen, text="Turn ends in:", x=430, y=650)
        DrawUtils.draw_label(screen, text="Turn ends in:", x=1050, y=650)

        self.draw_timer_based_on_turn(screen)

    def draw_timer_based_on_turn(self, screen):
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
        left_time = int(self.player.turn_end_time - time.time())
        return left_time if left_time >= 0 else 0

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
