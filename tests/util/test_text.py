import pygame
from gameoflife.util.text import InfoText


def test_info_text_init():
    pygame.font.init()
    info_text = InfoText("Test Text", 16)
    assert info_text.text == "Test Text"
    assert info_text.fontsize == 16
    assert info_text.color == (150, 150, 150)
    assert info_text.image.get_alpha() == 255


def test_info_text_default_alpha():
    pygame.font.init()
    info_text = InfoText("Test Text", 16)
    assert info_text.image.get_alpha() == 255


def test_info_text_alpha():
    pygame.font.init()
    info_text = InfoText("Test Text", 16, alpha=True)
    assert info_text.image.get_alpha() == 150


def test_info_text_update():
    pygame.font.init()
    info_text = InfoText("Test Text", 16)
    info_text.update("New Text")
    assert info_text.text == "New Text"


def test_info_text_position():
    pygame.font.init()
    info_text = InfoText("Test Text", 16)
    assert info_text.rect == (0, 0)
    info_text.set_position((25, 25))
    assert info_text.rect == (25, 25)
