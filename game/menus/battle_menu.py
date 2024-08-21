import pygame
import json
import time
import game.menus as menus
from game.visuals.visual_board import VisualBoard

ASK_RECEIVE_SHOT_EVENT = pygame.USEREVENT + 3


class BattleMenu(menus.Menu):
    def __init__(self, player):
        super().__init__()
        self.player = player
        pygame.time.set_timer(ASK_RECEIVE_SHOT_EVENT, 1000)

    def draw(self, screen):
        super().draw(screen)
        self.player.board.draw(screen)
        self.player.enemy_board_view.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if self.player.is_turn:
                if self.is_click_within_enemy_board(pos):
                    self.send_shot_command(pos)

        if event.type == ASK_RECEIVE_SHOT_EVENT:
            if not self.player.is_turn:
                self.player.ask_to_receive_shot()

        self.is_battle_over()

    def is_click_within_enemy_board(self, pos):
        return self.player.enemy_board_view.is_position_in_board(pos)

    def is_battle_over(self):
        pass

    def send_shot_command(self, pos):
        row, col = self.player.enemy_board_view.get_row_col_by_mouse(pos)

        if self.player.enemy_board_view.is_coordinate_shot_at(row, col):
            return

        self.player.shot(row, col)
