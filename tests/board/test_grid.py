from collections import Counter

from gameoflife.board.cell import Cell
from gameoflife.board.grid import (
    Grid,
    count_neighbors,
)


def test_count_neighbors() -> None:
    cell = Counter({(56, 28): 1, (57, 28): 1})
    pos = (56, 28)

    result = count_neighbors(cell, pos)

    assert result["alive"] == 1
    assert result["dead"] == [
        (55, 27),
        (55, 28),
        (55, 29),
        (56, 27),
        (56, 29),
        (57, 27),
        (57, 29),
    ]


def test_init_cell_value(grid: Grid) -> None:
    assert grid.cell == Counter()


def test_init_cell_sprite_value(grid: Grid) -> None:
    assert grid.cell_sprite == {}


def test_init_run_value(grid: Grid) -> None:
    assert grid.run is False


def test_init_deaths_value(grid: Grid) -> None:
    assert grid.deaths == 0


def test_init_generation_value(grid: Grid) -> None:
    assert grid.generation == 0


def test_start(grid: Grid) -> None:
    assert grid.run is False
    grid.start()
    assert grid.run is True


def test_stop(grid: Grid) -> None:
    assert grid.run is False
    grid.start()
    assert grid.run is True
    grid.stop()
    assert grid.run is False


def test_reset(grid: Grid) -> None:
    # Initialize with some random values.
    grid.start()
    grid.deaths = 1234
    grid.generation = 4567

    for i in range(10):
        grid.cell[(i, i)] = 0
        grid.cell_sprite[(i, i)] = Cell()

    # Reset and test if everything now is set to default values.
    grid.reset()

    assert grid.run is False
    assert grid.deaths == 0
    assert grid.generation == 0
    assert grid.cell == Counter()
    assert grid.cell_sprite == {}


def test_delete_cell(grid: Grid) -> None:
    limit = 10
    key = (5, 5)

    for i in range(limit):
        grid.cell[(i, i)] = 1
        grid.cell_sprite[(i, i)] = Cell()

    # Before delete.
    assert grid.cell[key] == 1
    assert key in grid.cell_sprite
    assert len(grid.cell) == limit

    grid.delete_cell(key)

    # After delete.
    assert grid.cell[key] == 0
    assert key not in grid.cell_sprite
    assert len(grid.cell) == limit - 1


def test_update_deaths(grid: Grid) -> None:
    start = 1
    end = 5

    assert grid.deaths == 0

    for i in range(start, end + 1):
        grid.update_deaths()
        assert grid.deaths == i

    assert grid.deaths == 5


def test_update(grid: Grid) -> None:
    grid.cell = Counter({(56, 28): 1, (57, 28): 1})
    grid.cell_sprite = {(56, 28): Cell(), (57, 28): Cell()}
    grid.deaths = 0
    grid.generation = 0

    grid.update()

    # Values after one generation.
    assert grid.run is False
    assert grid.deaths == 2
    assert grid.generation == 1
    assert grid.cell == Counter()
    assert grid.cell_sprite == {}
