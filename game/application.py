import pygame
from game.visuals.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, APPLICATION_TITLE
from game.visuals.visual_board import VisualBoard
from game.visuals.utils.buttons import ShuffleButton
from time import sleep

FPS = 60


class Application:
    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        pygame.init()
        pygame.display.set_caption(APPLICATION_TITLE)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.board = VisualBoard(10, 40)
        self.shuffle_button = ShuffleButton(x=700, y=300)

    def run(self):
        running = True
        print(self.board)

        while running:
            self.clock.tick(FPS)
            self.screen.fill((241, 250, 238))
            self.board.draw(self.screen)

            if self.shuffle_button.is_active(self.screen):
                self.board.random_shuffle_ships()
                self.board.draw(self.screen)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.board.is_position_in_board(pos):
                        row, col = self.board.get_row_col_by_mouse(pos)
                        print(row, col)


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
