import pygame
import game.visuals.utils.colors as colors
from game.visuals.utils.buttons import BasicButton
import game.menus as menus

from game.visuals.utils.draw_utils import DrawUtils


class BattleEndMenu(menus.Menu):
    def __init__(self, player, opponent_name):
        super().__init__()

        self.player = player
        self.opponent_name = opponent_name

        self.exit_room_button = BasicButton(x=490, y=630, text="Exit room")
        self.ending_message = self.get_ending_message()

        player.request_enemy_board()

    def draw(self, screen):
        super().draw(screen)

        self.player.board.draw(screen)
        self.player.enemy_board_view.draw(screen)
        DrawUtils.apply_color_overlay(screen, color=colors.TILE_MAIN_COLOR)

        DrawUtils.draw_centered_message_with_background(
            screen,
            title_text=self.ending_message[0],
            subtitle_text=self.ending_message[1],
        )
        self.exit_room_button.draw(screen)

    def get_ending_message(self):
        if self.player.is_winner:
            return (
                "You are victorious!",
                f"Congratulations {self.player.name} you destroyed your opponent {self.opponent_name}!",
            )

        return (
            "Defeat!",
            f"Better luck next time {self.player.name}, the win goes to {self.opponent_name}!",
        )

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.exit_room_button.is_active():
                self.next_menu = menus.StartMenu(self.player.name)
