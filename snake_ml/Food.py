import numpy as np

class Food:
    def __init__(self, x, y) -> None:
        self.pos = np.array((x,y))
        pass