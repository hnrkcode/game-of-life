import pygame

from gameoflife import settings


class Overlay(pygame.sprite.Sprite):
    """Overlay background."""

    def __init__(self) -> None:
        super().__init__()
        self.color = settings.OVERLAY_COLOR
        image = pygame.Surface([settings.WIDTH, settings.HEIGHT])
        image.set_alpha(225)
        image.fill(self.color)
        self.image = image
        self.rect = image.get_rect()
