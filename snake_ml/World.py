import pygame
import time
import numpy as np
from Snake import Snake
from Config import *

check_errors = pygame.init()


class World:

    fpsController = pygame.time.Clock()

    def __init__(self, n_snakes=1, maxRender=10) -> None:

        self.nSnakes = n_snakes
        self.maxRender = maxRender

        self.snakes = [Snake((GRID_WIDTH, GRID_HEIGHT), render=True)
                       for _ in range(n_snakes - 1)]

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.display.set_caption("SNAKEE")

    def drawBackground(self) -> None:
        self.screen.fill(text_bg_color)
        rect = (LEFT_MARGIN, TOP_MARGIN, WIDTH - 2 *
                LEFT_MARGIN, HEIGHT - 2*TOP_MARGIN)
        pygame.draw.rect(self.screen, background_color, rect)

    def drawSnakes(self) -> None:

        for i, snake in enumerate(self.snakes):
            if i >= self.maxRender:
                break

            if snake.render and snake.isAlive:
                snake.draw(self.screen)

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

    def renderFrame(self) -> None:
        self.drawBackground()
        self.drawSnakes()
        # self.drawVision()
        pygame.display.update()

    def restart(self) -> None:

        # Get the 10 snakes with the highest fitness

        self.snakes.sort(key=lambda x: x.fitness(), reverse=True)

        self.bestPastSnakes = self.snakes[:self.nSnakes//10]

        # Create new snakes

        newSnakes = []

        for snake in self.bestPastSnakes:
            for _ in range(self.nSnakes//10):
                newSnakes.append(snake.offspring())

        self.snakes = newSnakes

        if len(self.snakes) < self.nSnakes:
            self.snakes.append(Snake((GRID_WIDTH, GRID_HEIGHT), render=True))

    def gameOver(self) -> None:

        font = pygame.font.SysFont("monospace", 72)
        self.screen.fill(text_bg_color)
        label = font.render("GAME OVER", 1, text_color)
        self.screen.blit(label, (WIDTH/2 - label.get_width()/2,
                                 HEIGHT/2 - label.get_height()/2))
        pygame.display.update()
        self.restart()

    def start(self, autostep=True):
        if autostep:
            self.run()
        else:
            self.runStep()

    def runStep(self):

        running = True

        while running:
            for event in self.getEvents():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.step()
                    else:
                        self.handleInput(event)

            self.renderFrame()
            self.fpsController.tick(FPS)

    def run(self) -> None:
        running = True

        start_time = time.time()
        prev_time = start_time

        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    self.handleInput(event)

            current_time = time.time()

            if current_time - prev_time > 1/SPEED:
                prev_time = current_time
                self.step()

            self.renderFrame()
            pygame.time.Clock().tick(FPS)

    def handleInput(self, event) -> None:
        if event.key == pygame.K_UP:
            self.snakes[-1].direction = np.array([0, -1])
        elif event.key == pygame.K_RIGHT:
            self.snakes[-1].direction = np.array([1, 0])
        elif event.key == pygame.K_DOWN:
            self.snakes[-1].direction = np.array([0, 1])
        elif event.key == pygame.K_LEFT:
            self.snakes[-1].direction = np.array([-1, 0])

    def step(self) -> None:
        for snake in self.snakes:
            if snake.isAlive:
                snake.move()

        if not any(list(map(lambda x: x.isAlive, self.snakes))):
            self.gameOver()
