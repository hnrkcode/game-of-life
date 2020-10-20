import pygame

from gameoflife import settings
from gameoflife.util import text


class Modal(pygame.sprite.Sprite):
    """Modal background."""

    def __init__(self):
        super().__init__()

        # Make the modal's size 75 % of the screen size.
        width = int(settings.WIDTH * 0.55)
        height = int(settings.HEIGHT * 0.55)
        size = [width, height]

        # Position the modal in the center of the screen.
        pos = [int((settings.WIDTH - width) / 2), int((settings.HEIGHT - height) / 2)]

        self.color = settings.MODAL_COLOR
        self.image = pygame.Surface(size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        # Content inside modal.
        content = [
            text.InfoText("CONTROLS", 35, [(width / 2) - 40, 20]),
            # Keyboard controls.
            text.InfoText("Keyboard controls", 20, [80, 75]),
            text.InfoText("Pause:", 15, [80, 100]),
            text.InfoText("P", 15, [180, 100]),
            text.InfoText("Reset:", 15, [80, 120]),
            text.InfoText("R", 15, [180, 120]),
            text.InfoText("Fullscreen:", 15, [80, 140]),
            text.InfoText("F11", 15, [180, 140]),
            text.InfoText("Choose pattern:", 15, [80, 160]),
            text.InfoText("Up/Down", 15, [180, 160]),
            text.InfoText("Quit:", 15, [80, 180]),
            text.InfoText("ESC", 15, [180, 180]),
            # Mouse controls.
            text.InfoText("Mouse controls", 20, [80, 210]),
            text.InfoText("Draw cells:", 15, [80, 235]),
            text.InfoText("Left", 15, [180, 235]),
            text.InfoText("Erase cells:", 15, [80, 255]),
            text.InfoText("Right", 15, [180, 255]),
            text.InfoText("Choose pattern:", 15, [80, 275]),
            text.InfoText("Scroll", 15, [180, 275]),
            text.InfoText("Paste pattern:", 15, [80, 295]),
            text.InfoText("hold ctrl + left click", 15, [180, 295]),
        ]

        for data in content:
            self.image.blit(data.image, data.rect)
