"""
Module for the ship placement menu in the game. The `ShipPlacementMenu` class allows players to place ships on
their board, shuffle ship positions, and mark the board as ready for the next phase. It also handles
dragging and dropping ships, as well as interactions with buttons.
"""

import pygame
from game.visuals.utils.buttons import BasicButton
from game.menus.menu import Menu
from game.visuals.utils import colors
from game.visuals.utils.draw_utils import DrawUtils
from game.menus.battle_menu import BattleMenu


class ShipPlacementMenu(Menu):
    """
    Ship placement menu where players can place ships, shuffle their positions, and mark their board as ready.
    Handles ship dragging, placement validation, and displays waiting messages.
    """

    IS_OPPONENT_READY_EVENT = pygame.USEREVENT + 1
    WAITING_MESSAGE_UPDATE_EVENT = pygame.USEREVENT + 2

    def __init__(self, menus_evolution, player, room_id, opponent_name):
        """
        Initialize the ShipPlacementMenu with buttons for shuffling ships, marking readiness, and handling
        ship placement.

        Args:
            menus_evolution (list): List of menus in the evolution stack.
            player (Player): The player instance managing ship placement.
            room_id (str): The ID of the current room.
            opponent_name (str): The name of the opponent.
        """
        super().__init__(menus_evolution, message_x=697, message_y=538)
        self.add_self_to_evolution()

        self.player = player
        self.room_id = room_id
        self.opponent_name = opponent_name

        self.shuffle_button = BasicButton(x=600, y=558, text="Shuffle")
        self.start_button = BasicButton(x=950, y=558, text="Ready")

        self.dragging_ship = None
        self.original_row = 0
        self.original_col = 0

        self.waiting_dots = 0

        pygame.time.set_timer(self.IS_OPPONENT_READY_EVENT, 2000)
        pygame.time.set_timer(self.WAITING_MESSAGE_UPDATE_EVENT, 500)

    def handle_event(self, event):
        """
        Handle user events including mouse interactions and button clicks.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        super().handle_event(event)

        if self.player.has_sent_board:
            if event.type == self.IS_OPPONENT_READY_EVENT:
                self.handle_is_opponent_ready()

            elif event.type == self.WAITING_MESSAGE_UPDATE_EVENT:
                self.update_waiting_dots()

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.on_mouse_button_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.on_mouse_button_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self.on_mouse_motion()

            if self.shuffle_button.is_active():
                self.player.board.random_shuffle_ships()

            if self.start_button.is_active() and self.can_continue():
                self.handle_sending_board()

    def handle_is_opponent_ready(self):
        """
        Handle the event where the opponent is ready. Transitions to the BattleMenu if the opponent is ready.
        """
        response = self.player.is_opponent_ready()

        if response["status"] == "success":
            self.next_menu = BattleMenu(self.menus_evolution, self.player, self.opponent_name)

    def handle_sending_board(self):
        """
        Handle sending the board to the opponent. Disables the buttons once the board is sent.
        """
        response = self.player.send_board()
        if response["status"] == "error":
            self.show_message(response["message"])
            return

        self.start_button.set_disabled(True)
        self.shuffle_button.set_disabled(True)
        print("Wait for opponent to send board!")

    def update_waiting_dots(self):
        """
        Update the waiting message dots to indicate the waiting status.
        """
        self.waiting_dots = (self.waiting_dots + 1) % 4

    def get_waiting_message(self):
        """
        Get the message indicating that the player is waiting for the opponent to be ready.

        Returns:
            str: The waiting message with dynamic dots.
        """
        return f"Waiting for opponent to be ready{'.' * self.waiting_dots}"

    def on_mouse_button_down(self, event):
        """
        Handle mouse button down events for dragging and flipping ships.

        Args:
            event (pygame.event.Event): The event to handle.
        """
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

    def on_mouse_motion(self):
        """
        Handle mouse motion events for dragging ships.
        """
        if not self.dragging_ship:
            return

        pos = pygame.mouse.get_pos()
        if not self.player.board.is_position_in_board(pos):
            self.release_ship()
            return

        self.drag_ship(pos)

    def on_mouse_button_up(self, event):
        """
        Handle mouse button up events to release dragged ships.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if not (event.button == 1 and self.dragging_ship):
            return

        self.release_ship()

    def drag_ship(self, pos):
        """
        Handle dragging a ship to a new position.

        Args:
            pos (tuple): The new mouse position.
        """
        new_row, new_col = self.player.board.get_row_col_by_mouse(pos)
        self.dragging_ship.move(new_row, new_col, self.dragging_ship.is_horizontal)

        if self.player.board.is_ship_placement_valid(self.dragging_ship):
            self.dragging_ship.set_color(colors.SHIP_VALID_PLACEMENT_COLOR)
        else:
            self.dragging_ship.set_color(colors.SHIP_INVALID_PLACEMENT_COLOR)

        new_pos = self.player.board.get_tile_screen_placement(new_row, new_col)
        self.dragging_ship.update_visual_position(*new_pos)

    def release_ship(self):
        """
        Handle releasing a dragged ship. Places it back to its original position if placement is invalid.
        """
        if not self.player.board.is_ship_placement_valid(self.dragging_ship):
            self.dragging_ship.move(self.original_row, self.original_col, self.dragging_ship.is_horizontal)
            self.player.board.place_ship(self.dragging_ship)
            self.show_message("Cannot place ship there!")
        else:
            self.player.board.place_ship(self.dragging_ship)

        self.dragging_ship.set_color(colors.SHIP_DEFAULT_COLOR)
        self.dragging_ship = None

    def can_continue(self):
        """
        Check if the board setup is complete.

        Returns:
            bool: True if all ships are placed, False otherwise.
        """
        return len(self.player.board.unplaced_ships) == 0

    def draw(self, screen):
        """
        Draw the ship placement menu on the screen, including the board, buttons, and instructions.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        super().draw(screen)

        self.player.board.draw(screen)
        self.shuffle_button.draw(screen)
        self.start_button.draw(screen)

        DrawUtils.draw_title(screen, "Ship placement phase", x=920, y=120, font_size=64, glow_size=3)

        DrawUtils.draw_message(
            screen,
            "Left click and hold a ship to move it!",
            x=600,
            y=200,
            font_size=34,
            alignment="left",
        )
        DrawUtils.draw_message(
            screen,
            "Right click on a ship to flip it!",
            x=600,
            y=250,
            font_size=34,
            alignment="left",
        )
        DrawUtils.draw_message(
            screen,
            "Once the board is set up click the button 'Ready'.",
            x=600,
            y=300,
            font_size=34,
            alignment="left",
        )

        DrawUtils.draw_label(screen, f"Room ID: {self.room_id}", x=600, y=400, alignment="left")
        DrawUtils.draw_label(screen, f"Opponent: {self.opponent_name}", x=600, y=450, alignment="left")

        if self.player.has_sent_board:
            DrawUtils.apply_color_overlay(screen)
            DrawUtils.draw_message(
                screen,
                self.get_waiting_message(),
                x=600,
                y=500,
                font_size=34,
                alignment="left",
            )
