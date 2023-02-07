from Food import Food
import random
import numpy as np
import pygame
import copy

from NeuralNetwok import NeuralNetwork
from Config import *


class Snake:

    directions: np.ndarray = np.array(
        [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)])

    def __init__(self, grid: tuple[int, int], size: int = 3, speed: float = 3, render=False) -> None:
        self.body: list[tuple[int, int]] = [(2, grid[0]//2)]
        self.head: np.ndarray = np.array(self.body[0])

        self.size = size
        self.speed = speed
        self.render = render

        self.grid: tuple[int, int] = grid
        self.food: Food = self.getRandFood()

        self.brain = NeuralNetwork(8*3, (32, 32, 32), 4)
        self.color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        self.food.color = (self.color[0]*0.8,
                           self.color[1]*0.8, self.color[2]*0.8)

        self.isAlive = True
        self.mutationRate = 30
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
        self.head += self.directions[index]

        # Check if the snake ate food
        if (self.head == self.food.pos).all():
            self.size += 1
            self.food = self.getRandFood()

        # Check if the snake is too long
        if (len(self.body) > self.size - 1):
            self.body.pop()

        # Check if the snake went out of bounds
        if not (0 <= self.head[0] < self.grid[0] and 0 <= self.head[1] < self.grid[1]):
            self.isAlive = False

        # Check if the snake ate itself
        if (self.contains(self.head)):
            self.isAlive = False

        # Move the body
        self.body.insert(0, (self.head[0], self.head[1]))

    def getRandFood(self) -> Food:
        x = random.randint(0, self.grid[0] - 1)
        y = random.randint(0, self.grid[1] - 1)
        if self.contains((x, y)):
            return self.getRandFood()

        return Food(x, y)

    def contains(self, point) -> bool:
        if type(point) != np.ndarray:
            point = np.array(point)

        for body_part in self.body:
            if (body_part == point).all():
                return True
        return False

    def look(self) -> np.ndarray:

        vision = np.zeros(8*3)

        for i, direction in enumerate(self.directions):
            pos: np.ndarray = self.head + direction
            distance = 1
            food_dist = 0
            snake_dist = 0
            wall_dist = 0

            while (0 <= pos[0] < self.grid[0] and 0 <= pos[1] < self.grid[1]):
                if not food_dist and (self.food.pos == pos).all():
                    food_dist = distance

                if not snake_dist and self.contains(pos):
                    snake_dist = distance

                pos += direction
                distance += 1

            wall_dist = distance

            vision[i*3] = food_dist
            vision[i*3+1] = snake_dist
            vision[i*3+2] = wall_dist

        return vision

    def draw(self, screen) -> None:
        for segment in self.body:
            x, y = gridToPixel(segment)
            x += BODY_GAP/2
            y += BODY_GAP/2

            width = SEG_SIZE - BODY_GAP
            height = SEG_SIZE - BODY_GAP
            rect = (x, y, width, height)

            pygame.draw.rect(screen, self.color, rect)

            self.food.draw(screen)

    def fitness(self) -> float:
        return self.size + self.age ** 1/2

    def offspring(self) -> 'Snake':
        child = self.clone()
        child.brain.mutate(self.mutationRate)

        return child

    def clone(self) -> 'Snake':
        clone = Snake(self.grid, render=self.render)
        clone.brain = copy.deepcopy(self.brain)
        return clone
