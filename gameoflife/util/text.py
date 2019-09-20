import pygame

from gameoflife import settings


class InfoText(pygame.sprite.DirtySprite):
    def __init__(
        self,
        text,
        size,
        pos=(0, 0),
        font=settings.TEXT_FONT,
        color=settings.TEXT_COLOR,
    ):
        super().__init__()
        self.color = color
        self.text = text
        self.fontsize = size
        self._font = pygame.font.Font(font, size)
        self.image = self._font.render(text, 1, color)
        self.rect = pos

    def set_position(self, pos):
        self.rect = pos

    def update(self, text):
        self.image = self._font.render(text, 1, self.color)
