import pygame

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, APPLICATION_TITLE
from visual_board import VisualBoard

FPS = 60


class Application:
    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        pygame.init()
        pygame.display.set_caption(APPLICATION_TITLE)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.board = VisualBoard(10, 40)

    def run(self):
        running = True

        while running:
            self.clock.tick(FPS)
            self.board.drawTiles(self.screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = self.board.get_row_col_by_mouse(pos)
                    print(row, col)


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
