from Config import *
import pygame
import time
from Population import Population

check_errors = pygame.init()


class World:

    fpsController = pygame.time.Clock()

    def __init__(self, n_snakes=1) -> None:

        self.population = Population(n_snakes)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption("SNAKEE")

    def drawBackground(self) -> None:
        self.screen.fill(text_bg_color)
        rect = (LEFT_MARGIN, TOP_MARGIN, WIDTH - 2 *
                LEFT_MARGIN, HEIGHT - 2*TOP_MARGIN)
        pygame.draw.rect(self.screen, background_color, rect)

    def drawBestSnake(self) -> None:
        self.population.snakes[0].draw(self.screen)

        # def drawVision(self) -> None:
        #     for i, distance in enumerate(self.vision):
        #         direction = self.snake.directions[i//3]
        #         if distance == 0:
        #             continue
        #
        #         pos_x = self.snake.body[0][0] + direction[0] * distance
        #         pos_y = self.snake.body[0][1] + direction[1] * distance
        #
        #         offset = [direction[0] * self.SEG_SIZE /
        #                   2, direction[1] * self.SEG_SIZE/2]
        #
        #         x, y = self.gridToPixel((pos_x, pos_y))
        #         x += self.SEG_SIZE/2 - offset[0]
        #         y += self.SEG_SIZE/2 - offset[1]
        #
        #         x2, y2 = self.gridToPixel(self.snake.head)
        #         x2 += self.SEG_SIZE/2 + offset[0]
        #         y2 += self.SEG_SIZE/2 + offset[1]
        #
        #         pygame.draw.circle(self.screen, (255, 0, 0), (x, y), 5)
        #         pygame.draw.line(self.screen, (255, 0, 0), (x, y), (x2, y2), 1)

    def renderFrame(self) -> None:
        self.drawBackground()
        self.drawBestSnake()
        # self.drawVision()
        pygame.display.update()

    def run(self) -> None:
        running = True

        start_time = time.time()
        prev_time = start_time

        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

            self.step()

            self.renderFrame()
            pygame.time.Clock().tick(FPS)

    def step(self) -> None:
        for snake in self.population.snakes:
            if snake.isAlive:
                snake.move()

        if not any(list(map(lambda x: x.isAlive, self.population.snakes))):
            self.population.createNextGeneration()
