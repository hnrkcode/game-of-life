import pytest

from gameoflife.pattern.blueprint import get_patterns
from gameoflife.board.grid import Grid
from gameoflife.board import Board
from gameoflife.board.cell import Cell


@pytest.fixture()
def patterns() -> dict[str, list[list[int]]]:
    patterns = get_patterns()

    return patterns


@pytest.fixture()
def grid() -> Grid:
    grid = Grid()

    return grid


@pytest.fixture()
def board() -> Board:
    board = Board()

    return board


@pytest.fixture()
def cell() -> Cell:
    pos = (260, 50)
    cell = Cell(pos)

    return cell
