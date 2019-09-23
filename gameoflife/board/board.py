import pygame

from gameoflife import settings


class Board(pygame.sprite.Sprite):
    """Grid background."""

    def __init__(self):
        super().__init__()
        self.color = settings.DEAD
        self.image = pygame.Surface(
            [settings.BOARD_WIDTH_SIZE, settings.BOARD_HEIGHT_SIZE]
        )
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = [settings.BOARD_X_POS, settings.BOARD_Y_POS]
