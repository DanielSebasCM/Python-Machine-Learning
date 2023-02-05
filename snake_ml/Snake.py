from Food import Food
import random


class Snake:

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

    def __init__(self, grid: tuple[int, int], size: int = 3, speed: float = 3) -> None:
        self.size = size
        self.body = [(2, grid[0]//2)]
        self.head = self.body[0]
        self.direction = [1, 0]
        self.speed = speed
        self.grid = grid
        self.food = self.getRandFood()
        pass

    def move(self):

        # Move the head
        self.head = (self.head[0] + self.direction[0],
                     self.head[1] + self.direction[1])

        # Check if the snake ate food
        if self.head == self.food.pos:
            self.size += 1
            self.food = self.getRandFood()

        # Check if the snake is too long
        if (len(self.body) > self.size):
            self.body.pop()

        # Check if the snake went out of bounds
        if not (0 <= self.head[0] < self.grid[0] and 0 <= self.head[1] < self.grid[1]):
            raise Exception("Snake went out of bounds")

        # Check if the snake ate itself
        if (self.contains(self.head)):
            raise Exception("Snake ate itself")

        # Move the body
        self.body.insert(0, self.head)

    def getRandFood(self):
        x = random.randint(0, self.grid[0] - 1)
        y = random.randint(0, self.grid[1] - 1)
        if self.contains((x, y)):
            return self.getRandFood()

        return Food(x, y)

    def contains(self, point) -> bool:
        for body_part in self.body:
            if (body_part == point):
                return True
        return False

    def look(self):

        vision = []

        for direction in self.directions:
            pos = self.head[0] + direction[0], self.head[1] + direction[1]
            distance = 1
            food_dist = 0
            snake_dist = 0
            wall_dist = 0
            while (0 <= pos[0] < self.grid[0] and 0 <= pos[1] < self.grid[1]):
                if not food_dist and self.food.pos == pos:
                    food_dist = distance
                if not snake_dist and self.contains(pos):
                    snake_dist = distance

                pos = pos[0] + direction[0], pos[1] + direction[1]
                distance += 1

            wall_dist = distance

            vision.append(food_dist)
            vision.append(snake_dist)
            vision.append(wall_dist)

        return vision
