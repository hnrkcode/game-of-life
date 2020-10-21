import pygame

from gameoflife import settings
from gameoflife.util.text import InfoText


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
            InfoText("CONTROLS", size=settings.H2, pos=[(width / 2) - 40, 20]),
            # Keyboard controls.
            InfoText("Keyboard controls", size=settings.H4, pos=[80, 75]),
            InfoText("Pause:", size=settings.TEXT, pos=[80, 100]),
            InfoText("P", size=settings.TEXT, pos=[180, 100]),
            InfoText("Reset:", size=settings.TEXT, pos=[80, 120]),
            InfoText("R", size=settings.TEXT, pos=[180, 120]),
            InfoText("Fullscreen:", size=settings.TEXT, pos=[80, 140]),
            InfoText("F11", size=settings.TEXT, pos=[180, 140]),
            InfoText("Choose pattern:", size=settings.TEXT, pos=[80, 160]),
            InfoText("Up/Down", size=settings.TEXT, pos=[180, 160]),
            InfoText("Quit:", size=settings.TEXT, pos=[80, 180]),
            InfoText("ESC", size=settings.TEXT, pos=[180, 180]),
            # Mouse controls.
            InfoText("Mouse controls", size=settings.H4, pos=[80, 210]),
            InfoText("Draw cells:", size=settings.TEXT, pos=[80, 235]),
            InfoText("Left", size=settings.TEXT, pos=[180, 235]),
            InfoText("Erase cells:", size=settings.TEXT, pos=[80, 255]),
            InfoText("Right", size=settings.TEXT, pos=[180, 255]),
            InfoText("Choose pattern:", size=settings.TEXT, pos=[80, 275]),
            InfoText("Scroll", size=settings.TEXT, pos=[180, 275]),
            InfoText("Paste pattern:", size=settings.TEXT, pos=[80, 295]),
            InfoText("hold ctrl + left click", size=settings.TEXT, pos=[180, 295]),
        ]

        for data in content:
            self.image.blit(data.image, data.rect)
