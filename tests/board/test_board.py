import unittest

from gameoflife import settings
from gameoflife.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_init_color_is_dead(self):
        self.assertTupleEqual(self.board.color, settings.DEAD)

    def test_board_size(self):
        size = (settings.BOARD_WIDTH_SIZE, settings.BOARD_HEIGHT_SIZE)
        self.assertTupleEqual(self.board.rect.size, size)

    def test_board_position(self):
        pos = (settings.BOARD_X_POS, settings.BOARD_Y_POS)
        self.assertTupleEqual(self.board.rect.topleft, pos)
