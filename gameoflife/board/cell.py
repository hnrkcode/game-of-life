import math

import pygame

from gameoflife import settings

GEN1_RANGE = (1, 5)
GEN2_RANGE = (5, 10)
GEN3_RANGE = (10, 50)
GEN4_RANGE = (50, 100)
GEN5_RANGE = (100, math.inf)


class Cell(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__()
        self.color = settings.ALIVE
        self.image = pygame.Surface([settings.CELL_SIZE, settings.CELL_SIZE])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.generation = 0

    def next_gen(self) -> None:
        """Update the generations the cell has existed and colorize it."""
        self.generation += 1
        if GEN1_RANGE[0] < self.generation <= GEN1_RANGE[1]:
            self.color = settings.GEN1
            self.image.fill(self.color)
        elif GEN2_RANGE[0] < self.generation <= GEN2_RANGE[1]:
            self.color = settings.GEN2
            self.image.fill(self.color)
        elif GEN3_RANGE[0] < self.generation <= GEN3_RANGE[1]:
            self.color = settings.GEN3
            self.image.fill(self.color)
        elif GEN4_RANGE[0] < self.generation <= GEN4_RANGE[1]:
            self.color = settings.GEN4
            self.image.fill(self.color)
        elif GEN5_RANGE[0] < self.generation <= GEN5_RANGE[1]:
            self.color = settings.GEN5
            self.image.fill(self.color)
