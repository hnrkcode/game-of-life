from collections import Counter

from gameoflife import settings
from gameoflife.board.cell import Cell
from gameoflife.board.grid import (
    calc_pos,
    calc_size,
    count_neighbors,
    is_inside_grid,
)


def test_pattern_size():
    pattern = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    width, height = (
        len(pattern[0]) * settings.CELL_SIZE,
        len(pattern) * settings.CELL_SIZE,
    )
    assert calc_size(pattern) == (width, height)


def test_pattern_inside_grids_boundary():
    pattern = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

    # Setup where it should work to paste the pattern based on it's size.
    w, h = calc_size(pattern)
    pos_topleft_corner = (settings.MIN_X, settings.MIN_Y)
    pos_topright_corner = (
        settings.MAX_X - w + settings.CELL_SIZE,
        settings.MIN_Y,
    )
    pos_bottomleft_corner = (
        settings.MIN_X,
        settings.MAX_Y - h + settings.CELL_SIZE,
    )
    pos_bottomright_corner = (settings.MAX_X - w, settings.MAX_Y - h)

    assert is_inside_grid(pos_topleft_corner, pattern) == True
    assert is_inside_grid(pos_topright_corner, pattern) == True
    assert is_inside_grid(pos_bottomleft_corner, pattern) == True
    assert is_inside_grid(pos_bottomright_corner, pattern) == True


def test_pattern_outside_grids_boundary():
    pattern = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    assert is_inside_grid((0, 0), pattern) == False


def test_calculate_position():
    assert calc_pos((123, 456)), (120, 450) == True


def test_count_neighbors():
    cell = Counter({(560, 280): 1, (570, 280): 1})
    pos = (560, 280)

    result = count_neighbors(cell, pos)

    assert result["alive"] == 1
    assert result["dead"] == [
        (550, 270),
        (550, 280),
        (550, 290),
        (560, 270),
        (560, 290),
        (570, 270),
        (570, 290),
    ]


def test_init_cell_value(grid):
    assert grid.cell == Counter()


def test_init_cell_sprite_value(grid):
    assert grid.cell_sprite == Counter()


def test_init_run_value(grid):
    assert grid.run == False


def test_init_deaths_value(grid):
    assert grid.deaths == 0


def test_init_generation_value(grid):
    assert grid.generation == 0


def test_start(grid):
    assert grid.run == False
    grid.start()
    assert grid.run == True


def test_stop(grid):
    assert grid.run == False
    grid.start()
    assert grid.run == True
    grid.stop()
    assert grid.run == False


def test_reset(grid):
    # Initialize with some random values.
    grid.start()
    grid.deaths = 1234
    grid.generation = 4567

    for i in range(10):
        grid.cell[(i, i)] = 0
        grid.cell_sprite[(i, i)] = 0

    # Reset and test if everything now is set to default values.
    grid.reset()

    assert grid.run == False
    assert grid.deaths == 0
    assert grid.generation == 0
    assert grid.cell == Counter()
    assert grid.cell_sprite == Counter()


def test_delete_cell(grid):
    limit = 10
    key = (5, 5)

    for i in range(limit):
        grid.cell[(i, i)] = 1
        grid.cell_sprite[(i, i)] = 1

    # Before delete.
    assert grid.cell[key] == 1
    assert grid.cell_sprite[key] == 1
    assert len(grid.cell) == limit

    grid.delete_cell(key)

    # After delete.
    assert grid.cell[key] == 0
    assert grid.cell_sprite[key] == 0
    assert len(grid.cell) == limit - 1


def test_update_deaths(grid):
    start = 1
    end = 5

    assert grid.deaths == 0

    for i in range(start, end + 1):
        grid.update_deaths()
        assert grid.deaths == i

    assert grid.deaths == 5


def test_update(grid):
    grid.cell = Counter({(560, 280): 1, (570, 280): 1})
    grid.cell_sprite = Counter(
        {(560, 280): Cell((560, 280)), (570, 280): Cell((570, 280))}
    )
    grid.deaths = 0
    grid.generation = 0

    grid.update()

    # Values after one generation.
    assert grid.run == False
    assert grid.deaths == 2
    assert grid.generation == 1
    assert grid.cell == Counter()
    assert grid.cell_sprite == Counter()
