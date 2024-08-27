import pygame
import json
import time
import game.menus as menus
from game.visuals.visual_board import VisualBoard


class BattleMenu(menus.Menu):
    ASK_RECEIVE_SHOT_EVENT = pygame.USEREVENT + 5

    def __init__(self, player, opponent_name):
        super().__init__()
        self.player = player
        self.opponent_name = opponent_name

        pygame.time.set_timer(self.ASK_RECEIVE_SHOT_EVENT, 1000)

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

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if self.player.is_turn:
                if self.is_click_within_enemy_board(pos):
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
