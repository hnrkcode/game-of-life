import pytest

from gameoflife.board import Board
from gameoflife.board.cell import Cell
from gameoflife.board.grid import Grid
from gameoflife.pattern.blueprint import get_patterns


@pytest.fixture()
def patterns() -> dict[str, list[list[int]]]:
    return get_patterns()


@pytest.fixture()
def grid() -> Grid:
    return Grid()


@pytest.fixture()
def board() -> Board:
    return Board()


@pytest.fixture()
def cell() -> Cell:
    return Cell(pos=(260, 50))
