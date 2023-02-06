from Food import Food
import random
import numpy as np
from NeuralNetwok import NeuralNetwork


class Snake:

    directions: np.ndarray = np.array(
        [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)])
    direction = np.array([1, 0])
    isAlive = True

    def __init__(self, grid: tuple[int, int], size: int = 3, speed: float = 3) -> None:
        self.size: int = size
        self.body: list[tuple[int, int]] = [(2, grid[0]//2)]
        self.head: np.ndarray = np.array(self.body[0])
        self.speed: float = speed
        self.grid: tuple[int, int] = grid
        self.food: Food = self.getRandFood()
        pass

    def move(self, direction: np.ndarray) -> None:
        # Move the head
        self.head = self.head + direction

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
        self.body.insert(0, self.head)

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
