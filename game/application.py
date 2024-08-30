"""Module that represents the client-side application for the game."""

import pygame
from game.visuals.utils import constants
from game.menus.start_menu import StartMenu


class Application:  # pylint: disable=R0903
    """
    A class to manage the game application's main loop and event handling using Pygame.

    Initializes Pygame, sets up the display, and manages the main loop to handle events and rendering.
    """

    def __init__(
        self,
        width=constants.WINDOW_WIDTH,
        height=constants.WINDOW_HEIGHT,
        fps=constants.FPS,
    ):
        """
        Initializes the Application instance, setting up the Pygame environment and the main menu.

        Args:
            width (int): The width of the game window. Defaults to constants.WINDOW_WIDTH.
            height (int): The height of the game window. Defaults to constants.WINDOW_HEIGHT.
            fps (int): The frames per second for the game loop. Defaults to constants.FPS.
        """
        pygame.init()
        pygame.display.set_caption(constants.APPLICATION_TITLE)
        self.screen = pygame.display.set_mode((width, height))
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.menu = StartMenu()

        self.running = True

    def run(self):
        """
        Starts and runs the main loop of the application.

        Continuously handles events, updates the menu, and renders the display until the application is closed.
        """
        while self.running:
            self.clock.tick(self.fps)
            self._handle_events()
            self._draw_menu()

        pygame.quit()

    def _handle_events(self):
        """
        Handles Pygame events such as user inputs and window events.

        Updates the state of the application based on events and changes the menu if needed.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.menu.handle_event(event)

            if self.menu.next_menu:
                self.menu = self.menu.next_menu

    def _draw_menu(self):
        """
        Draws the current menu to the screen and updates the display.

        Calls the draw method on the current menu and updates the Pygame display.
        """
        self.menu.draw(self.screen)
        pygame.display.update()


def main():
    """
    Entry point for running the application.

    Creates an instance of the Application class and starts its main loop.
    """
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
