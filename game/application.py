import pygame

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, APPLICATION_TITLE
from board import Board

FPS = 60


class Application:
    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        pygame.init()
        pygame.display.set_caption(APPLICATION_TITLE)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.board = Board(0, 0)

    def run(self):
        running = True

        while running:
            self.clock.tick(FPS)
            self.board.drawBoard(self.screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
