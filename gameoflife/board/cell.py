import pygame

from gameoflife import settings


class Cell(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.color = settings.ALIVE
        self.image = pygame.Surface([settings.CELL_SIZE, settings.CELL_SIZE])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.generation = 0

    def next_gen(self):
        """Update the generations the cell has existed and colorize it."""

        self.generation += 1
        if 1 < self.generation <= 5:
            self.color = settings.GEN1
            self.image.fill(self.color)
        elif 5 < self.generation <= 10:
            self.color = settings.GEN2
            self.image.fill(self.color)
        elif 10 < self.generation <= 50:
            self.color = settings.GEN3
            self.image.fill(self.color)
        elif 50 < self.generation <= 100:
            self.color = settings.GEN4
            self.image.fill(self.color)
        elif 100 < self.generation:
            self.color = settings.GEN5
            self.image.fill(self.color)
