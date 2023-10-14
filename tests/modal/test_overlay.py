import pygame
from gameoflife import settings
from gameoflife.modal.overlay import Overlay


def test_overlay_init():
    pygame.init()
    overlay = Overlay()

    assert overlay.color == settings.OVERLAY_COLOR
    assert overlay.image.get_alpha() == 225
    assert overlay.rect.topleft == (0, 0)
    assert overlay.rect.size == (settings.WIDTH, settings.HEIGHT)
