import pygame
import time
import numpy as np
from Snake import Snake


class Game:
    check_errors = pygame.init()

    ASPECT_RATIO = 16/9

    HEIGHT = 480
    WIDTH = HEIGHT * ASPECT_RATIO

    GRID_HEIGHT = 15
    GRID_WIDTH = 15

    SEG_SIZE = min(HEIGHT/GRID_HEIGHT, WIDTH/GRID_WIDTH)
    LEFT_MARGIN = (WIDTH - GRID_WIDTH*SEG_SIZE)/2
    TOP_MARGIN = (HEIGHT - GRID_HEIGHT*SEG_SIZE)/2

    BODY_GAP = SEG_SIZE*0.03

    SPEED = 3  # Grid squares per second
    FPS = 60

    snake_color = 0x788374
    food_color = 0xaa644d
    text_color = 0xf5e9bf
    text_bg_color = 0x372a39
    background_color = 0xf5e9bf

    def __init__(self) -> None:
        self.snake = Snake((self.GRID_WIDTH, self.GRID_HEIGHT))
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # self.vision = self.snake.look()
        score = 0
        pygame.display.set_caption("SNAKEE")

    def drawBackground(self) -> None:
        self.screen.fill(self.text_bg_color)
        rect = (self.LEFT_MARGIN, self.TOP_MARGIN, self.WIDTH - 2 *
                self.LEFT_MARGIN, self.HEIGHT - 2*self.TOP_MARGIN)
        pygame.draw.rect(self.screen, self.background_color, rect)

    def drawSnake(self) -> None:
        for segment in self.snake.body:
            x, y = self.gridToPixel(segment)
            x += self.BODY_GAP/2
            y += self.BODY_GAP/2

            width = self.SEG_SIZE - self.BODY_GAP
            height = self.SEG_SIZE - self.BODY_GAP
            rect = (x, y, width, height)

            pygame.draw.rect(self.screen, self.snake_color, rect)

    def drawFood(self) -> None:
        x, y = self.gridToPixel(self.snake.food.pos)
        x += self.BODY_GAP/2
        y += self.BODY_GAP/2

        width = self.SEG_SIZE - self.BODY_GAP
        height = self.SEG_SIZE - self.BODY_GAP
        rect = (x, y, width, height)

        pygame.draw.rect(self.screen, self.food_color, rect)

    def drawScore(self) -> None:
        font = pygame.font.SysFont("monospace", 72)
        label = font.render(str(self.snake.size), 1, self.text_color)
        self.screen.blit(label, (self.WIDTH/2 - label.get_width()/2,
                                 self.HEIGHT/2 - label.get_height()/2))

    # def drawVision(self) -> None:
    #     for i, distance in enumerate(self.vision):
    #         direction = self.snake.directions[i//3]
    #         if distance == 0:
    #             continue

    #         pos_x = self.snake.body[0][0] + direction[0] * distance
    #         pos_y = self.snake.body[0][1] + direction[1] * distance

    #         offset = [direction[0] * self.SEG_SIZE /
    #                   2, direction[1] * self.SEG_SIZE/2]

    #         x, y = self.gridToPixel((pos_x, pos_y))
    #         x += self.SEG_SIZE/2 - offset[0]
    #         y += self.SEG_SIZE/2 - offset[1]

    #         x2, y2 = self.gridToPixel(self.snake.head)
    #         x2 += self.SEG_SIZE/2 + offset[0]
    #         y2 += self.SEG_SIZE/2 + offset[1]

    #         pygame.draw.circle(self.screen, (255, 0, 0), (x, y), 5)
    #         pygame.draw.line(self.screen, (255, 0, 0), (x, y), (x2, y2), 1)

    def gridToPixel(self, grid_pos) -> tuple[int, int]:
        x = grid_pos[0] * self.SEG_SIZE + self.LEFT_MARGIN
        y = grid_pos[1] * self.SEG_SIZE + self.TOP_MARGIN
        return (x, y)

    def renderFrame(self) -> None:
        self.drawBackground()
        self.drawSnake()
        self.drawFood()
        # self.drawVision()
        pygame.display.update()

    def restart(self) -> None:
        self.snake = Snake((self.GRID_WIDTH, self.GRID_HEIGHT))

    def gameOver(self) -> None:
        font = pygame.font.SysFont("monospace", 72)
        self.screen.fill(self.text_bg_color)
        label = font.render("GAME OVER", 1, self.text_color)
        self.screen.blit(label, (self.WIDTH/2 - label.get_width()/2,
                                 self.HEIGHT/2 - label.get_height()/2))
        pygame.display.update()
        time.sleep(3)
        self.restart()

    def run(self) -> None:
        running = True

        start_time = time.time()
        prev_time = start_time

        while running:
            # for loop through the event queue
            for event in pygame.event.get():

                # Check for QUIT event
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    self.handleInput(event)

            current_time = time.time()

            if current_time - prev_time > 1/self.SPEED:
                prev_time = current_time
                self.step()

                self.score = len(self.snake.body) * 100

            self.renderFrame()
            pygame.time.Clock().tick(self.FPS)

    def handleInput(self, event) -> None:
        if event.key == pygame.K_UP:
            self.snake.direction = np.array([0, -1])
        elif event.key == pygame.K_RIGHT:
            self.snake.direction = np.array([1, 0])
        elif event.key == pygame.K_DOWN:
            self.snake.direction = np.array([0, 1])
        elif event.key == pygame.K_LEFT:
            self.snake.direction = np.array([-1, 0])

    def step(self) -> np.ndarray:
        self.snake.move(self.snake.direction)

        if not self.snake.isAlive:
            self.gameOver()

        return self.snake.look()


game = Game()

running = True

while running:
    # for loop through the event queue
    for event in pygame.event.get():

        # Check for QUIT event
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.step()
            else:
                game.handleInput(event)

    game.renderFrame()
    pygame.time.Clock().tick(game.FPS)
