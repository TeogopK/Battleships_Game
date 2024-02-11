import pygame


class Application:
    def __init__(self, width=1280, height=720):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

    def draw_player(self, player):
        self.screen.fill("white")
        pygame.draw.circle(self.screen, player.color,
                           player.player_pos, player.size)
        pygame.display.flip()

    def run(self, player):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

            self.draw_player(player)
            player.move()

            self.clock.tick(60)


class Player:
    def __init__(self, screen, color):
        self.player_pos = pygame.Vector2(
            screen.get_width() / 2, screen.get_height() / 2
        )
        self.color = color
        self.size = 40
        self.velocity = 15

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_pos.y -= self.velocity
        if keys[pygame.K_s]:
            self.player_pos.y += self.velocity
        if keys[pygame.K_a]:
            self.player_pos.x -= self.velocity
        if keys[pygame.K_d]:
            self.player_pos.x += self.velocity


def main():
    app = Application()
    player1 = Player(app.screen, "blue")
    app.run(player1)


if __name__ == "__main__":
    main()
