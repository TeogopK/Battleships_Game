import pygame


class BattleMenu:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

        self.enemy_attack_position = (0, 0)

    def draw(self, screen):
        screen.fill((0, 0, 0))
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

            if self.player.choose_attack(row, col, self.enemy):
                self.player.end_turn()
                self.enemy_attack()
                self.player.take_turn()

    def is_click_within_enemy_board(self, pos):
        return self.enemy.board.is_position_in_board(pos)

    def enemy_attack(self):
        row, col = self.enemy_attack_position

        self.enemy.choose_attack(row, col, self.player)
        self.enemy_attack_position = self.get_next_attack_position(row, col)

        self.player.take_turn()

    def get_next_attack_position(self, row, col):
        col += 1
        if col >= self.player.board.columns_count:
            col = 0
            row += 1

        if row >= self.player.board.rows_count:
            row = 0
            col = 0

        return row, col

    def check_game_over(self):
        if self.player.are_all_ships_sunk():
            print(f"{self.player.name} loses!")
            return True
        if self.enemy.are_all_ships_sunk():
            print(f"{self.player.name} wins!")
            return True
        return False
