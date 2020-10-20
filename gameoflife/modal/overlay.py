import pygame

from gameoflife import settings


class Overlay(pygame.sprite.Sprite):
    """Overlay background."""

    def __init__(self):
        super().__init__()
        self.color = settings.OVERLAY_COLOR
        self.image = pygame.Surface([settings.WIDTH, settings.HEIGHT])
        self.image.set_alpha(225)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]
