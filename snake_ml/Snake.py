class Snake:

    def __init__(self, grid: tuple[int, int], size: int = 3, speed: float = 3) -> None:
        self.size = size
        self.body = [(2, grid[0]//2)]
        self.head = self.body[0]
        self.direction = [1, 0]
        self.speed = speed
        self.grid = grid
        pass

    def contains(self, point) -> bool:
        for body_part in self.body:
            if (body_part == point):
                return True
        return False

    def move(self):

        new_head = (self.head[0] + self.direction[0],
                    self.head[1] + self.direction[1])
        self.head = new_head

        if (self.contains(new_head)):
            raise Exception("Snake ate itself")

        if not (0 <= new_head[0] < self.grid[0] and 0 <= new_head[1] < self.grid[1]):
            raise Exception("Snake went out of bounds")

        self.body.insert(0, new_head)

        if (len(self.body) > self.size):
            self.body.pop()

        pass
