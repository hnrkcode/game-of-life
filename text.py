import pygame
import settings


class InfoText(pygame.sprite.DirtySprite):

    def __init__(self, fontsize, text, pos=(0, 0), font=settings.FONT):
        super().__init__()
        self.text = text
        self.fontsize = fontsize
        self._font = pygame.font.Font(font, self.fontsize)
        self.image = self._font.render(self.text, 1, settings.TEXT_COLOR)
        self.rect = pos

    def set_position(self, pos):
        self.rect = pos

    def update(self, text):
        self.image = self._font.render(text, 1, settings.TEXT_COLOR)
