import pygame

from gameoflife import settings


class InfoText(pygame.sprite.DirtySprite):
    def __init__(
        self,
        text: str | None,
        size: int,
        pos: tuple[int, int] = (0, 0),
        font: str = settings.TEXT_FONT,
        color: tuple[int, int, int] = settings.TEXT_COLOR,
        alpha: bool = False,
    ) -> None:
        super().__init__()
        self.color = color
        self.text = text
        self.fontsize = size
        self._font = pygame.font.Font(font, size)
        self.image = self._font.render(text, 1, color)
        self.rect = self.image.get_rect(topleft=pos)

        if alpha:
            self.image.set_alpha(150)

    def set_position(self, pos: tuple[int, int]) -> None:
        self.rect.topleft = pos

    def update(self, text: str | None) -> None:
        self.text = text
        self.image = self._font.render(self.text, 1, self.color)
