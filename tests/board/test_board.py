from gameoflife import settings


def test_init_color_is_dead(board):
    assert board.color == settings.DEAD


def test_board_size(board):
    size = (settings.BOARD_WIDTH_SIZE, settings.BOARD_HEIGHT_SIZE)
    assert board.rect.size == size


def test_board_position(board):
    pos = (settings.BOARD_X_POS, settings.BOARD_Y_POS)
    assert board.rect.topleft == pos
