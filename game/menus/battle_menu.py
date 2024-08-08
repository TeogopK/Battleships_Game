import pygame


class BattleMenu:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.stop_showing_menu = False

    def draw(self, screen):
        self.player.board.draw(screen)
        self.enemy.board.draw_for_enemy(screen)
        pygame.display.flip()

    def handle_event(self, event):
        if not self.player.is_turn:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            if not self.is_click_within_enemy_board(pos):
                return

            row, col = self.enemy.board.get_row_col_by_mouse(pos)

            if self.enemy.board.is_coordinate_shot_at(row, col):
                return

            hit = self.enemy.board.register_shot(row, col)

            if hit:
                print("Hit! Player gets another turn.")
            else:
                self.player.end_turn()
                self.enemy.perform_attack(self.player)
                self.player.take_turn()

        self.is_battle_over()

    def is_click_within_enemy_board(self, pos):
        return self.enemy.board.is_position_in_board(pos)

    def is_battle_over(self):
        if self.player.are_all_ships_sunk() or self.enemy.are_all_ships_sunk():
            print("GAME OVER")
            self.stop_showing_menu = True
