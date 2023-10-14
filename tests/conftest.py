import pytest

from gameoflife.pattern.blueprint import get_patterns
from gameoflife.board.grid import Grid
from gameoflife.board import Board
from gameoflife.board.cell import Cell


@pytest.fixture()
def patterns():
    patterns = get_patterns()

    return patterns


@pytest.fixture()
def grid():
    grid = Grid()

    return grid


@pytest.fixture()
def board():
    board = Board()

    return board


@pytest.fixture()
def cell():
    pos = (260, 50)
    cell = Cell(pos)

    return cell
