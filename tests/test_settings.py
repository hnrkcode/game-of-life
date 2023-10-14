from pathlib import PurePath

from gameoflife import settings


def test_fps_is_30():
    assert settings.FPS == 30


def test_base_dir():
    assert PurePath(settings.BASE_DIR).name == PurePath(__file__).parent.parent.name


def test_data_dir():
    assert PurePath(settings.DATA_DIR).name == "data"


def test_image_dir():
    assert PurePath(settings.IMAGE_DIR).name == "images"


def test_font_dir():
    assert PurePath(settings.FONT_DIR).name == "fonts"


def test_text_dir():
    assert PurePath(settings.TEXT_DIR).name == "text"


def test_icon_file():
    assert PurePath(settings.ICON_FILE).name == "logo.png"


def test_font_files():
    assert PurePath(settings.HEADER_FONT).name == "LLPIXEL3.ttf"
    assert PurePath(settings.TEXT_FONT).name == "Rheiborn_Sans_Clean.ttf"


def test_patterns_file():
    assert PurePath(settings.PATTERN_LIST).name == "patterns.txt"


def test_text_color():
    assert settings.TEXT_COLOR == (150, 150, 150)


def test_background_color():
    assert settings.BG_COLOR == (19, 19, 19)


def test_modal_color():
    assert settings.MODAL_COLOR == (40, 40, 40)


def test_overlay_color():
    assert settings.OVERLAY_COLOR == (10, 10, 10)


def test_dead_cell_color():
    assert settings.DEAD == (27, 27, 27)


def test_alive_cell_color():
    assert settings.ALIVE == (150, 150, 150)


def test_generation_colors():
    assert settings.GEN1 == (40, 160, 255)
    assert settings.GEN2 == (0, 255, 206)
    assert settings.GEN3 == (233, 255, 131)
    assert settings.GEN4 == (255, 141, 61)
    assert settings.GEN5 == (232, 0, 25)


def test_paste_on_color():
    assert settings.PASTE_ON == (138, 226, 52)


def test_paste_off_color():
    assert settings.PASTE_OFF == (239, 41, 41)


def test_active_menu_pattern_color():
    assert settings.ACTIVE == (255, 255, 255)


def test_width():
    assert settings.WIDTH == 1280


def test_height():
    assert settings.HEIGHT == 720


def test_window_size():
    assert settings.WINDOW_SIZE == (settings.WIDTH, settings.HEIGHT)


def test_cell_size():
    assert settings.CELL_SIZE == 10


def test_board_position():
    board_pos = (settings.BOARD_X_POS, settings.BOARD_Y_POS)
    assert board_pos == (250, 50)


def test_grid_border_limits():
    assert settings.MIN_X == 250
    assert settings.MAX_X == 250 + 980 - 10
    assert settings.MIN_Y == 50
    assert settings.MAX_Y == 50 + 620 - 10


def test_total_cells():
    assert settings.TOTAL_CELLS == int(980 / 10 * 620 / 10)
    assert isinstance(settings.TOTAL_CELLS, int)


def test_board_size():
    board_size = (settings.BOARD_WIDTH_SIZE, settings.BOARD_HEIGHT_SIZE)
    board_width = 980 / 10
    board_height = 620 / 10
    assert board_size == (980, 620)
    assert settings.BOARD_WIDTH == board_width
    assert settings.BOARD_HEIGHT == board_height
    assert isinstance(settings.BOARD_WIDTH, int)
    assert isinstance(settings.BOARD_HEIGHT, int)


def test_mouse_button_settings():
    assert settings.LEFT_CLICK == (1, 0, 0)
    assert settings.RIGHT_CLICK == (0, 0, 1)
    assert settings.SCROLL_DOWN == 5
    assert settings.SCROLL_UP == 4


def test_text_sizes():
    assert settings.H1 == 100
    assert settings.H2 == 35
    assert settings.H3 == 25
    assert settings.H4 == 20
    assert settings.TEXT == 15
