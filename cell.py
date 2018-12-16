import pygame
import settings

class Cell(pygame.sprite.Sprite):
    """Individual cells on the grid."""

    def __init__(self, pos):
        super().__init__()
        self.color = settings.DEAD
        self.image = pygame.Surface([settings.CELL, settings.CELL])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.alive = False
        self.generation = 0

    def custom_state(self, state):
        """Switch to the chosen state."""
        self.alive = state
        if self.alive:
            self.color = settings.ALIVE
            self.image.fill(self.color)
        else:
            self.color = settings.DEAD
            self.image.fill(self.color)

    def change_state(self):
        """Switch to the opposite state."""
        if self.alive:
            self.alive = False
            self.color = settings.DEAD
            self.image.fill(self.color)
        else:
            self.alive = True
            self.color = settings.ALIVE
            self.image.fill(self.color)

    def next_gen(self):
        """Update the generations the cell has existed and colorize it."""
        if self.alive:
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
        else:
            self.reset()

    def reset(self):
        """Set the generation back to zero if cell has died."""
        self.generation = 0
        self.color = settings.DEAD
        self.image.fill(self.color)
