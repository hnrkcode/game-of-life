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
        alpha=False,
    ):
        super().__init__()
        self.color = color
        self.text = text
        self.fontsize = size
        self._font = pygame.font.Font(font, size)
        self.image = self._font.render(text, 1, color)
        self.rect = pos

        if alpha:
            self.image.set_alpha(150)

    def set_position(self, pos):
        self.rect = pos

    def update(self, text):
        self.text = text
        self.image = self._font.render(self.text, 1, self.color)
