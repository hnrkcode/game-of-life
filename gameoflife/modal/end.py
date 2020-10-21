import math
import pygame

from gameoflife import settings
from gameoflife.util.text import InfoText


class End(pygame.sprite.Sprite):
    """The end screen."""

    def __init__(self):
        super().__init__()
        self.color = settings.OVERLAY_COLOR
        self.image = pygame.Surface(
            [settings.BOARD_WIDTH_SIZE, settings.BOARD_HEIGHT_SIZE]
        )
        self.image.set_alpha(150)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = [settings.BOARD_X_POS, settings.BOARD_Y_POS]

        # Determines how much the letter is being moved.
        self.y = 0

    def update(self):

        self.image.fill(self.color)

        letters = (
            InfoText("E", size=settings.H1, pos=[0, 0]),
            InfoText("N", size=settings.H1, pos=[50, 0]),
            InfoText("D", size=settings.H1, pos=[100, 0]),
        )

        text_width = sum(map(lambda letter: letter.image.get_width(), letters))
        center = int(settings.BOARD_WIDTH_SIZE / 2) - (text_width / 2)

        movement = int(10 * math.sin(self.y)) + 10
        self.y += 1

        for letter in letters:
            letter.rect[0] += center
            letter.rect[1] = int(settings.BOARD_WIDTH_SIZE * 0.25) + movement
            self.image.blit(letter.image, letter.rect)
