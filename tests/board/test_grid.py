import unittest
from collections import Counter

from gameoflife import settings
from gameoflife.board.cell import Cell
from gameoflife.board.grid import (
    Grid,
    calc_pos,
    calc_size,
    count_neighbors,
    is_inside_grid,
)


class TestCalcSize(unittest.TestCase):
    def test_pattern_size(self):
        pattern = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        width, height = (
            len(pattern[0]) * settings.CELL_SIZE,
            len(pattern) * settings.CELL_SIZE,
        )
        self.assertTupleEqual(calc_size(pattern), (width, height))


class TestIsInsideGrid(unittest.TestCase):
    def setUp(self):
        self.pattern = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

        # Setup where it should work to paste the pattern based on it's size.
        w, h = calc_size(self.pattern)
        self.pos_topleft_corner = (settings.MIN_X, settings.MIN_Y)
        self.pos_topright_corner = (
            settings.MAX_X - w + settings.CELL_SIZE,
            settings.MIN_Y,
        )
        self.pos_bottomleft_corner = (
            settings.MIN_X,
            settings.MAX_Y - h + settings.CELL_SIZE,
        )
        self.pos_bottomright_corner = (settings.MAX_X - w, settings.MAX_Y - h)

    def test_pattern_inside_grids_boundary(self):
        self.assertTrue(is_inside_grid(self.pos_topleft_corner, self.pattern))
        self.assertTrue(is_inside_grid(self.pos_topright_corner, self.pattern))
        self.assertTrue(is_inside_grid(self.pos_bottomleft_corner, self.pattern))
        self.assertTrue(is_inside_grid(self.pos_bottomright_corner, self.pattern))

    def test_pattern_outside_grids_boundary(self):
        self.assertFalse(is_inside_grid((0, 0), self.pattern))


class TestCalcPos(unittest.TestCase):
    def test_calculate_position(self):
        self.assertTupleEqual(calc_pos((123, 456)), (120, 450))


class TestCountNeighbors(unittest.TestCase):
    def test_count_neighbors(self):

        cell = Counter({(560, 280): 1, (570, 280): 1})
        pos = (560, 280)

        result = count_neighbors(cell, pos)

        self.assertEqual(result["alive"], 1)
        self.assertListEqual(
            result["dead"],
            [
                (550, 270),
                (550, 280),
                (550, 290),
                (560, 270),
                (560, 290),
                (570, 270),
                (570, 290),
            ],
        )


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.grid = Grid()

    def test_init_cell_value(self):
        self.assertEqual(self.grid.cell, Counter())

    def test_init_cell_sprite_value(self):
        self.assertEqual(self.grid.cell_sprite, Counter())

    def test_init_run_value(self):
        self.assertFalse(self.grid.run)

    def test_init_deaths_value(self):
        self.assertEqual(self.grid.deaths, 0)

    def test_init_generation_value(self):
        self.assertEqual(self.grid.generation, 0)

    def test_start(self):
        self.assertFalse(self.grid.run)
        self.grid.start()
        self.assertTrue(self.grid.run)

    def test_stop(self):
        self.assertFalse(self.grid.run)
        self.grid.start()
        self.assertTrue(self.grid.run)
        self.grid.stop()
        self.assertFalse(self.grid.run)

    def test_reset(self):
        # Initialize with some random values.
        self.grid.start()
        self.grid.deaths = 1234
        self.grid.generation = 4567

        for i in range(10):
            self.grid.cell[(i, i)] = 0
            self.grid.cell_sprite[(i, i)] = 0

        # Reset and test if everything now is set to default values.
        self.grid.reset()

        self.assertFalse(self.grid.run)
        self.assertEqual(self.grid.deaths, 0)
        self.assertEqual(self.grid.generation, 0)
        self.assertEqual(self.grid.cell, Counter())
        self.assertEqual(self.grid.cell_sprite, Counter())

    def test_delete_cell(self):
        limit = 10
        key = (5, 5)

        for i in range(limit):
            self.grid.cell[(i, i)] = 1
            self.grid.cell_sprite[(i, i)] = 1

        # Before delete.
        self.assertEqual(self.grid.cell[key], 1)
        self.assertEqual(self.grid.cell_sprite[key], 1)
        self.assertEqual(len(self.grid.cell), limit)

        self.grid.delete_cell(key)

        # After delete.
        self.assertEqual(self.grid.cell[key], 0)
        self.assertEqual(self.grid.cell_sprite[key], 0)
        self.assertEqual(len(self.grid.cell), limit - 1)

    def test_update_deaths(self):
        start = 1
        end = 5

        self.assertEqual(self.grid.deaths, 0)

        for i in range(start, end + 1):
            self.grid.update_deaths()
            self.assertEqual(self.grid.deaths, i)

        self.assertEqual(self.grid.deaths, 5)

    def test_update(self):

        self.grid.cell = Counter({(560, 280): 1, (570, 280): 1})
        self.grid.cell_sprite = Counter(
            {(560, 280): Cell((560, 280)), (570, 280): Cell((570, 280))}
        )
        self.grid.deaths = 0
        self.grid.generation = 0

        self.grid.update()

        # Values after one generation.
        self.assertFalse(self.grid.run)
        self.assertEqual(self.grid.deaths, 2)
        self.assertEqual(self.grid.generation, 1)
        self.assertEqual(self.grid.cell, Counter())
        self.assertEqual(self.grid.cell_sprite, Counter())