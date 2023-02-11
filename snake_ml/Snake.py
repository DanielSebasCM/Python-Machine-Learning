from Config import *

from Food import Food
import random
import pygame

from NeuralNetwok import NeuralNetwork


class Snake:

    directions: list[tuple[int, int]] = [
        (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    size = 4
    score = 0

    def __init__(self, createBrain=True) -> None:
        self.body: list[tuple[int, int]] = [(2, GRID_WIDTH//2)]
        self.head = self.body[0]

        self.food: Food = self.getRandFood()

        if createBrain:
            self.brain = NeuralNetwork(8*3, [32, 32, 32], 4)

        self.color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        self.food.color = (int(self.color[0]*0.8),
                           int(self.color[1]*0.8),
                           int(self.color[2]*0.8))

        self.isAlive = True
        self.age = 0
        self.lifeSpan = 200

    def move(self) -> None:
        # Move the head
        self.age += 1
        self.lifeSpan -= 1

        if self.lifeSpan <= 0:
            self.isAlive = False
            return

        vision = self.look()
        probabilities = self.brain.forward(vision.reshape(1, vision.size))

        index = np.argmax(probabilities)
        self.head = (self.head[0] + self.directions[index][0],
                     self.head[1] + self.directions[index][1])

        # Check if the snake ate food
        if (self.head == self.food.pos):
            self.size += 1
            self.food = self.getRandFood()
            self.lifeSpan += 100
            self.score += 1

        # Check if the snake is too long
        if (len(self.body) > self.size - 1):
            self.body.pop()

        # Check if the snake went out of bounds
        if not (0 <= self.head[0] < GRID_WIDTH and 0 <= self.head[1] < GRID_HEIGHT):
            self.isAlive = False

        # Check if the snake ate itself
        if (self.contains(self.head)):
            self.isAlive = False

        # Move the body
        self.body.insert(0, (self.head[0], self.head[1]))

    def getRandFood(self) -> Food:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if self.contains((x, y)):
            return self.getRandFood()

        return Food(x, y)

    def contains(self, point: tuple[int, int]) -> bool:

        for body_part in self.body:
            if (body_part == point):
                return True
        return False

    def look(self) -> ndarray:

        vision = np.zeros(8*3)

        for i, direction in enumerate(self.directions):
            pos = self.head[0] + direction[0], self.head[1] + direction[1]
            distance = 1
            food_dist = 0
            snake_dist = 0
            wall_dist = 0

            while (0 <= pos[0] < GRID_WIDTH and 0 <= pos[1] < GRID_HEIGHT):
                if not food_dist and (self.food.pos == pos):
                    food_dist = distance

                if not snake_dist and self.contains(pos):
                    snake_dist = distance

                pos = pos[0] + direction[0], pos[1] + direction[1]
                distance += 1

            wall_dist = distance

            vision[i] = food_dist
            vision[i+8] = snake_dist
            vision[i+16] = wall_dist

        return vision

    def draw(self, screen) -> None:
        for segment in self.body:
            x, y = gridToPixel(segment)
            x += BODY_GAP//2
            y += BODY_GAP//2

            width = SEG_SIZE - BODY_GAP
            height = SEG_SIZE - BODY_GAP
            rect = (x, y, width, height)

            pygame.draw.rect(screen, self.color, rect)

            self.food.draw(screen)

    def getFitness(self) -> float:
        fitness = self.age**2
        if self.score < 10:
            fitness *= 2**self.score
        else:
            fitness *= 2**10 * self.score

        return fitness

    def copy(self) -> "Snake":
        snake = Snake()
        snake.brain = self.brain.copy()
        return snake

    def mutate(self, mutationRate: float) -> None:
        self.brain.mutate(mutationRate)

    def crossover(self, partner: "Snake") -> "Snake":
        child = Snake(createBrain=False)
        child.brain = self.brain.crossover(partner.brain)
        return child
