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
        image = self._font.render(text, True, color)
        self.image = image
        self.rect = image.get_rect(topleft=pos)

        if alpha:
            image.set_alpha(150)

    @property
    def surface(self) -> pygame.Surface:
        image = self.image
        if image is None:
            msg = "Text sprite has no image"
            raise ValueError(msg)
        return image

    @property
    def bounds(self) -> pygame.Rect | pygame.FRect:
        rect = self.rect
        if rect is None:
            msg = "Text sprite has no rectangle"
            raise ValueError(msg)
        return rect

    def set_position(self, pos: tuple[int, int]) -> None:
        self.bounds.topleft = pos

    def update(self, text: str | None) -> None:
        self.text = text
        self.image = self._font.render(self.text, True, self.color)
