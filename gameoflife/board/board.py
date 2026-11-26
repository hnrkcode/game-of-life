import pygame

from gameoflife import settings


class Board(pygame.sprite.Sprite):
    """Grid background."""

    def __init__(self) -> None:
        super().__init__()
        self.color = settings.DEAD
        image = pygame.Surface([settings.BOARD_WIDTH_SIZE, settings.BOARD_HEIGHT_SIZE])
        image.fill(self.color)
        self.image = image
        self.rect = image.get_rect(topleft=(settings.BOARD_X_POS, settings.BOARD_Y_POS))
