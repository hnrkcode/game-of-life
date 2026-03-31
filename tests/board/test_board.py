from gameoflife.board import Board
from gameoflife import settings


def test_init_color_is_dead(board: Board) -> None:
    assert board.color == settings.DEAD


def test_board_size(board: Board) -> None:
    size = (settings.BOARD_WIDTH_SIZE, settings.BOARD_HEIGHT_SIZE)
    assert board.rect.size == size


def test_board_position(board: Board) -> None:
    pos = (settings.BOARD_X_POS, settings.BOARD_Y_POS)
    assert board.rect.topleft == pos
