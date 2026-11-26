import math

import pygame

from gameoflife import settings
from gameoflife.util.text import InfoText


class ScreenText(pygame.sprite.Sprite):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = self.set_text(text)
        self.color = settings.OVERLAY_COLOR
        image = pygame.Surface([settings.BOARD_WIDTH_SIZE, settings.BOARD_HEIGHT_SIZE])
        image.set_alpha(150)
        image.fill(self.color)
        self.image = image
        self.rect = image.get_rect(topleft=(settings.BOARD_X_POS, settings.BOARD_Y_POS))

        # Determines how much the letter is being moved.
        self.y = 0

    def set_text(self, text: str) -> list[InfoText]:
        x, y = 0, 0
        letters = []

        for letter in list(text):
            letters.append(InfoText(letter, size=settings.H1, pos=(x, y), alpha=True))
            x += 50

        # Center text.
        text_width = sum(letter.surface.get_width() for letter in letters)
        center = int(settings.BOARD_WIDTH_SIZE / 2) - (text_width / 2)

        for letter in letters:
            letter.bounds[0] += center

        return letters

    def update(self) -> None:
        image = self.image
        if image is None:
            return
        image.fill(self.color)

        for letter in self.text:
            # Creates a wave effect for the letters horizontal position.
            movement = int(10 * math.sin(self.y)) + 10
            self.y += 1

            letter.bounds[1] = int(settings.BOARD_WIDTH_SIZE * 0.25) + movement
            image.blit(letter.surface, letter.bounds)
