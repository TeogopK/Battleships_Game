import pygame
from game.visuals.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, APPLICATION_TITLE
from game.visuals.visual_board import VisualBoard
from game.visuals.utils.buttons import ShuffleButton


class ShipPlacementMenu:
    def __init__(self):
        self.board = VisualBoard(10, 40)
        self.shuffle_button = ShuffleButton(x=700, y=300)
        self.dragging_ship = None
        self.original_row = 0
        self.original_col = 0

    def draw(self, screen):
        self.board.draw(screen)
        self.shuffle_button.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.on_mouse_button_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.on_mouse_button_up(event)
        elif event.type == pygame.MOUSEMOTION:
            self.on_mouse_motion(event)

        if self.shuffle_button.is_active():
            self.board.random_shuffle_ships()

    def on_mouse_button_down(self, event):
        pos = pygame.mouse.get_pos()

        if not self.board.is_position_in_board(pos):
            return

        row, col = self.board.get_row_col_by_mouse(pos)
        ship = self.board.get_ship_on_coord(row, col)

        if ship and event.button == 1:  # Left mouse button
            self.dragging_ship = ship
            self.original_row = ship.row
            self.original_col = ship.col
            self.board.remove_ship(self.dragging_ship)

        if ship and event.button == 3:  # Right mouse button
            self.board.flip_ship(ship)

    def on_mouse_motion(self, event):
        if not self.dragging_ship:
            return

        pos = pygame.mouse.get_pos()
        new_row, new_col = self.board.get_row_col_by_mouse(pos)
        self.dragging_ship.move(
            new_row, new_col, self.dragging_ship.is_horizontal)

        if self.board.is_ship_placement_valid(self.dragging_ship):
            self.dragging_ship.set_color((0, 255, 0))
        else:
            self.dragging_ship.set_color((255, 0, 0))

        new_pos = self.board.get_tile_screen_placement(new_row, new_col)
        self.dragging_ship.update_visual_position(*new_pos)

    def on_mouse_button_up(self, event):
        if not (event.button == 1 and self.dragging_ship):
            return

        if not self.board.is_ship_placement_valid(self.dragging_ship):
            self.dragging_ship.move(
                self.original_row, self.original_col, self.dragging_ship.is_horizontal)
            self.board.place_ship(self.dragging_ship)
            print("Cannot place ship here!")
        else:
            self.board.place_ship(self.dragging_ship)
        self.dragging_ship = None
