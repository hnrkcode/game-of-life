import math
import pygame

from gameoflife import settings
from gameoflife.util.text import InfoText


class ScreenText(pygame.sprite.Sprite):
    def __init__(self, text):
        super().__init__()
        self.text = self.set_text(text)
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

    def set_text(self, text):
        x, y = 0, 0
        letters = []

        for letter in list(text):
            letters.append(InfoText(letter, size=settings.H1, pos=[x, y], alpha=True))
            x += 50

        # Center text.
        text_width = sum(map(lambda letter: letter.image.get_width(), letters))
        center = int(settings.BOARD_WIDTH_SIZE / 2) - (text_width / 2)

        for letter in letters:
            letter.rect[0] += center

        return letters

    def update(self):
        self.image.fill(self.color)

        for letter in self.text:
            # Creates a wave effect for the letters horizontal position.
            movement = int(10 * math.sin(self.y)) + 10
            self.y += 1

            letter.rect[1] = int(settings.BOARD_WIDTH_SIZE * 0.25) + movement
            self.image.blit(letter.image, letter.rect)
