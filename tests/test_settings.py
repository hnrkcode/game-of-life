import os
import unittest

import gameoflife
from gameoflife import name, settings


class TestSettings(unittest.TestCase):
    def test_fps_is_30(self):
        self.assertEqual(settings.FPS, 30)

    def test_base_dir(self):
        self.assertEqual(os.path.basename(settings.BASE_DIR), "gameoflife")

    def test_data_dir(self):
        self.assertEqual(os.path.basename(settings.DATA_DIR), "data")

    def test_image_dir(self):
        self.assertEqual(os.path.basename(settings.IMAGE_DIR), "images")

    def test_font_dir(self):
        self.assertEqual(os.path.basename(settings.FONT_DIR), "fonts")

    def test_text_dir(self):
        self.assertEqual(os.path.basename(settings.TEXT_DIR), "text")

    def test_icon_file(self):
        self.assertRegex(os.path.basename(settings.ICON_FILE), "logo.png$")

    def test_font_files(self):
        self.assertRegex(
            os.path.basename(settings.HEADER_FONT), "[a-z0-9].ttf$"
        )
        self.assertRegex(os.path.basename(settings.TEXT_FONT), "[a-z0-9_].ttf$")

    def test_patterns_file(self):
        self.assertRegex(
            os.path.basename(settings.PATTERN_LIST), "patterns.txt$"
        )

    def test_text_color(self):
        self.assertEqual(settings.TEXT_COLOR, (150, 150, 150))

    def test_background_color(self):
        self.assertEqual(settings.BG_COLOR, (19, 19, 19))

    def test_dead_cell_color(self):
        self.assertEqual(settings.DEAD, (27, 27, 27))

    def test_alive_cell_color(self):
        self.assertEqual(settings.ALIVE, (150, 150, 150))

    def test_generation_colors(self):
        self.assertEqual(settings.GEN1, (40, 160, 255))
        self.assertEqual(settings.GEN2, (0, 255, 206))
        self.assertEqual(settings.GEN3, (233, 255, 131))
        self.assertEqual(settings.GEN4, (255, 141, 61))
        self.assertEqual(settings.GEN5, (232, 0, 25))

    def test_active_menu_pattern_color(self):
        self.assertEqual(settings.ACTIVE, (255, 255, 255))

    def test_window_size(self):
        self.assertEqual((settings.WIDTH, settings.HEIGHT), (1280, 720))

    def test_cell_size(self):
        self.assertEqual(settings.CELL_SIZE, 10)

    def test_board_position(self):
        board_pos = (settings.BOARD_X_POS, settings.BOARD_Y_POS)
        self.assertEqual(board_pos, (250, 50))

    def test_grid_border_limits(self):
        self.assertEqual(settings.MIN_X, 250)
        self.assertEqual(settings.MAX_X, 250 + 980 - 10)
        self.assertEqual(settings.MIN_Y, 50)
        self.assertEqual(settings.MAX_Y, 50 + 620 - 10)

    def test_total_cells(self):
        self.assertEqual(settings.TOTAL_CELLS, int(980 / 10 * 620 / 10))
        self.assertIsInstance(settings.TOTAL_CELLS, int)

    def test_board_size(self):
        board_size = (settings.BOARD_WIDTH_SIZE, settings.BOARD_HEIGHT_SIZE)
        board_width = 980 / 10
        board_height = 620 / 10
        self.assertEqual(board_size, (980, 620))
        self.assertEqual(settings.BOARD_WIDTH, board_width)
        self.assertEqual(settings.BOARD_HEIGHT, board_height)
        self.assertIsInstance(settings.BOARD_WIDTH, int)
        self.assertIsInstance(settings.BOARD_HEIGHT, int)

    def test_mouse_button_settings(self):
        self.assertEqual(settings.LEFT_CLICK, (1, 0, 0))
        self.assertEqual(settings.RIGHT_CLICK, (0, 0, 1))
        self.assertEqual(settings.SCROLL_DOWN, 5)
        self.assertEqual(settings.SCROLL_UP, 4)
