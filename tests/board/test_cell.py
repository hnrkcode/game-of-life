import unittest

from gameoflife import settings
from gameoflife.board.cell import Cell


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.pos = (260, 50)
        self.cell = Cell(self.pos)

    def test_init_color_is_alive(self):
        self.assertTupleEqual(self.cell.color, settings.ALIVE)

    def test_cell_size(self):
        size = (settings.CELL_SIZE, settings.CELL_SIZE)
        self.assertTupleEqual(self.cell.rect.size, size)

    def test_cell_position(self):
        self.assertTupleEqual(self.cell.rect.topleft, self.pos)

    def test_init_generation(self):
        self.assertEqual(self.cell.generation, 0)

    def test_first_generation_color(self):
        first_time = True

        for gen in range(1, 5):
            if first_time:
                self.cell.generation = gen
                first_time = False

            self.assertEqual(self.cell.generation, gen)
            self.cell.next_gen()
            cell_color = tuple(self.cell.image.get_at((0, 0)))
            self.assertTupleEqual(cell_color, (*settings.GEN1, 255))

    def test_second_generation_color(self):
        first_time = True

        for gen in range(5, 10):
            if first_time:
                self.cell.generation = gen
                first_time = False

            self.assertEqual(self.cell.generation, gen)
            self.cell.next_gen()
            cell_color = tuple(self.cell.image.get_at((0, 0)))
            self.assertTupleEqual(cell_color, (*settings.GEN2, 255))

    def test_third_generation_color(self):
        first_time = True

        for gen in range(10, 50):
            if first_time:
                self.cell.generation = gen
                first_time = False

            self.assertEqual(self.cell.generation, gen)
            self.cell.next_gen()
            cell_color = tuple(self.cell.image.get_at((0, 0)))
            self.assertTupleEqual(cell_color, (*settings.GEN3, 255))

    def test_fourth_generation_color(self):
        first_time = True

        for gen in range(50, 100):
            if first_time:
                self.cell.generation = gen
                first_time = False

            self.assertEqual(self.cell.generation, gen)
            self.cell.next_gen()
            cell_color = tuple(self.cell.image.get_at((0, 0)))
            self.assertTupleEqual(cell_color, (*settings.GEN4, 255))

    def test_fifth_generation_color(self):
        first_time = True

        for gen in range(100, 150):
            if first_time:
                self.cell.generation = gen
                first_time = False

            self.assertEqual(self.cell.generation, gen)
            self.cell.next_gen()
            cell_color = tuple(self.cell.image.get_at((0, 0)))
            self.assertTupleEqual(cell_color, (*settings.GEN5, 255))