from gameoflife.board.cell import Cell
from gameoflife.pattern.paste import PastePattern
from gameoflife.main import has_finished, is_pausable


def test_has_finished_returns_true_when_no_cells_alive_and_generation_greater_than_zero() -> None:
    grid = PastePattern()
    grid.generation = 1
    assert has_finished(grid) is True


def test_has_finished_returns_false_when_cells_alive() -> None:
    grid = PastePattern()
    grid.cell_sprite[(0, 0)] = Cell((0, 0))
    grid.generation = 1
    assert has_finished(grid) is False


def test_has_finished_returns_false_when_generation_zero() -> None:
    grid = PastePattern()
    assert has_finished(grid) is False


def test_has_finished_returns_false_when_cells_alive_and_generation_zero() -> None:
    grid = PastePattern()
    grid.cell_sprite[(0, 0)] = Cell((0, 0))
    assert has_finished(grid) is False


def test_is_pausable_returns_true_when_cells_alive_and_generation_greater_than_zero() -> None:
    grid = PastePattern()
    grid.cell_sprite[(0, 0)] = Cell((0, 0))
    grid.generation = 1
    assert is_pausable(grid) is True


def test_is_pausable_returns_false_when_no_cells_alive() -> None:
    grid = PastePattern()
    grid.generation = 1
    assert is_pausable(grid) is False


def test_is_pausable_returns_false_when_generation_zero() -> None:
    grid = PastePattern()
    assert is_pausable(grid) is False
