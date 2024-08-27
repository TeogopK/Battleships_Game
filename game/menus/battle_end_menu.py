import pygame
import game.visuals.utils.colors as colors
from game.visuals.utils.buttons import BasicButton
import game.menus as menus

from game.visuals.utils.shapes import DrawUtils


class BattleEndMenu(menus.Menu):
    def __init__(self, player, opponent_name):
        super().__init__()

        self.player = player
        self.opponent_name = opponent_name

        self.exit_room_button = BasicButton(x=550, y=630, text="Exit room")

        player.request_enemy_board()

    def draw(self, screen):
        super().draw(screen)

        self.player.board.draw(screen)
        self.player.enemy_board_view.draw(screen)
        self.exit_room_button.draw(screen)

        ending_message = self.get_ending_message()
        DrawUtils.draw_title(
            screen, ending_message[0], x=1, y=1, font_size=40, glow_size=6
        )
        DrawUtils.draw_title(
            screen, ending_message[1], x=1, y=50, font_size=30, glow_size=3
        )

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
