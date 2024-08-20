import pygame
from game.visuals.utils.buttons import BasicButton
from game.menus.battle_menu import BattleMenu
from game.menus.menu import Menu

import game.visuals.utils.colors as colors

IS_OPPONENT_READY_EVENT = pygame.USEREVENT + 2


class ShipPlacementMenu(Menu):
    def __init__(self, player, room_id):
        super().__init__()
        self.player = player
        self.room_id = room_id

        self.shuffle_button = BasicButton(x=700, y=300, text="Shuffle")
        self.start_button = BasicButton(x=700, y=400, text="Ready")

        self.dragging_ship = None
        self.original_row = 0
        self.original_col = 0

        self.next_menu = None
        pygame.time.set_timer(IS_OPPONENT_READY_EVENT, 2000)

    def draw(self, screen):
        super().draw(screen)
        self.player.board.draw(screen)
        self.shuffle_button.draw(screen)
        self.start_button.draw(screen)

    def handle_event(self, event):
        if self.player.has_sent_board:
            if event.type == IS_OPPONENT_READY_EVENT:
                self.handle_is_opponent_ready()

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.on_mouse_button_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.on_mouse_button_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self.on_mouse_motion(event)

            if self.shuffle_button.is_active():
                self.player.board.random_shuffle_ships()

            if self.start_button.is_active() and self.can_continue():
                self.handle_sending_board()

    def handle_is_opponent_ready(self):
        response = self.player.is_opponent_ready()

        if response["status"] == "success":
            self.next_menu = BattleMenu(self.player)

    def handle_sending_board(self):
        response = self.player.send_board()
        if response["status"] == "success":
            print("Wait for opponent to send board!")

    def on_mouse_button_down(self, event):
        pos = pygame.mouse.get_pos()

        if not self.player.board.is_position_in_board(pos):
            return

        row, col = self.player.board.get_row_col_by_mouse(pos)
        ship = self.player.board.get_ship_on_coord(row, col)

        if ship and event.button == 1:  # Left mouse button
            self.dragging_ship = ship
            self.original_row = ship.row
            self.original_col = ship.col
            self.player.board.remove_ship(self.dragging_ship)

        if ship and event.button == 3:  # Right mouse button
            self.player.board.flip_ship(ship)

    def on_mouse_motion(self, event):
        if not self.dragging_ship:
            return

        pos = pygame.mouse.get_pos()
        if not self.player.board.is_position_in_board(pos):
            self.release_ship()
            return

        self.drag_ship(pos)

    def on_mouse_button_up(self, event):
        if not (event.button == 1 and self.dragging_ship):
            return

        self.release_ship()

    def drag_ship(self, pos):
        new_row, new_col = self.player.board.get_row_col_by_mouse(pos)
        self.dragging_ship.move(new_row, new_col, self.dragging_ship.is_horizontal)

        if self.player.board.is_ship_placement_valid(self.dragging_ship):
            self.dragging_ship.set_color(colors.SHIP_VALID_PLACEMENT_COLOR)
        else:
            self.dragging_ship.set_color(colors.SHIP_INVALID_PLACEMENT_COLOR)

        new_pos = self.player.board.get_tile_screen_placement(new_row, new_col)
        self.dragging_ship.update_visual_position(*new_pos)

    def release_ship(self):
        if not self.player.board.is_ship_placement_valid(self.dragging_ship):
            self.dragging_ship.move(
                self.original_row, self.original_col, self.dragging_ship.is_horizontal
            )
            self.player.board.place_ship(self.dragging_ship)
            print("Cannot place ship here!")
        else:
            self.player.board.place_ship(self.dragging_ship)

        self.dragging_ship.set_color(colors.SHIP_DEFAULT_COLOR)
        self.dragging_ship = None

    def can_continue(self):
        return len(self.player.board.unplaced_ships) == 0
