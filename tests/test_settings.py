import unittest
from pathlib import PurePath

import gameoflife
from gameoflife import settings


class TestSettings(unittest.TestCase):
    def test_fps_is_30(self):
        self.assertEqual(settings.FPS, 30)

    def test_base_dir(self):
        self.assertEqual(PurePath(settings.BASE_DIR).name, "gameoflife")

    def test_data_dir(self):
        self.assertEqual(PurePath(settings.DATA_DIR).name, "data")

    def test_image_dir(self):
        self.assertEqual(PurePath(settings.IMAGE_DIR).name, "images")

    def test_font_dir(self):
        self.assertEqual(PurePath(settings.FONT_DIR).name, "fonts")

    def test_text_dir(self):
        self.assertEqual(PurePath(settings.TEXT_DIR).name, "text")

    def test_icon_file(self):
        self.assertRegex(PurePath(settings.ICON_FILE).name, "logo.png$")

    def test_font_files(self):
        self.assertRegex(PurePath(settings.HEADER_FONT).name, "[a-z0-9].ttf$")
        self.assertRegex(PurePath(settings.TEXT_FONT).name, "[a-z0-9_].ttf$")

    def test_patterns_file(self):
        self.assertRegex(PurePath(settings.PATTERN_LIST).name, "patterns.txt$")

    def test_text_color(self):
        self.assertTupleEqual(settings.TEXT_COLOR, (150, 150, 150))

    def test_background_color(self):
        self.assertTupleEqual(settings.BG_COLOR, (19, 19, 19))

    def test_modal_color(self):
        self.assertTupleEqual(settings.MODAL_COLOR, (40, 40, 40))

    def test_overlay_color(self):
        self.assertTupleEqual(settings.OVERLAY_COLOR, (10, 10, 10))

    def test_dead_cell_color(self):
        self.assertTupleEqual(settings.DEAD, (27, 27, 27))

    def test_alive_cell_color(self):
        self.assertTupleEqual(settings.ALIVE, (150, 150, 150))

    def test_generation_colors(self):
        self.assertTupleEqual(settings.GEN1, (40, 160, 255))
        self.assertTupleEqual(settings.GEN2, (0, 255, 206))
        self.assertTupleEqual(settings.GEN3, (233, 255, 131))
        self.assertTupleEqual(settings.GEN4, (255, 141, 61))
        self.assertTupleEqual(settings.GEN5, (232, 0, 25))
    
    def test_paste_on_color(self):
        self.assertTupleEqual(settings.PASTE_ON, (138, 226, 52))

    def test_paste_off_color(self):
        self.assertTupleEqual(settings.PASTE_OFF, (239, 41, 41))

    def test_active_menu_pattern_color(self):
        self.assertTupleEqual(settings.ACTIVE, (255, 255, 255))

    def test_width(self):
        self.assertEqual(settings.WIDTH, 1280)
    
    def test_height(self):
        self.assertEqual(settings.HEIGHT, 720)

    def test_window_size(self):
        self.assertTupleEqual(settings.WINDOW_SIZE, (settings.WIDTH, settings.HEIGHT))

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
        self.assertTupleEqual(settings.LEFT_CLICK, (1, 0, 0))
        self.assertTupleEqual(settings.RIGHT_CLICK, (0, 0, 1))
        self.assertEqual(settings.SCROLL_DOWN, 5)
        self.assertEqual(settings.SCROLL_UP, 4)

    def test_text_sizes(self):
        self.assertEqual(settings.H1, 100)
        self.assertEqual(settings.H2, 35)
        self.assertEqual(settings.H3, 25)
        self.assertEqual(settings.H4, 20)
        self.assertEqual(settings.TEXT, 15)