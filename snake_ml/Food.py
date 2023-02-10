import numpy as np
import pygame
from Config import *


class Food:

    color = food_color

    def __init__(self, x, y) -> None:
        self.pos = (x, y)
        pass

    def draw(self, screen) -> None:
        x, y = gridToPixel(self.pos)
        y += FOOD_GAP//2
        x += FOOD_GAP//2

        width = SEG_SIZE - FOOD_GAP
        height = SEG_SIZE - FOOD_GAP
        rect = (x, y, width, height)

        pygame.draw.rect(screen, self.color, rect)
