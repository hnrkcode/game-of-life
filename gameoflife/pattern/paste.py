import pygame

from gameoflife import settings
from gameoflife.board.cell import Cell
from gameoflife.board.grid import Grid, calc_pos

from . import blueprint
from .select import PatternSelector


class PastePattern(Grid):
    """Read in predefined patterns and paste them on the grid."""

    def __init__(self):
        super().__init__()
        self.select = PatternSelector()
        self.pattern = blueprint.get_patterns()
        for name in self.pattern.keys():
            self.select.append((name, self.paste))

    def is_inside_grid(self, pos, matrix):
        """Make sure the pattern is pasted inside the grids boundary."""

        x, y = pos
        w, h = self.calc_size(matrix)

        left = settings.MIN_X
        up = settings.MIN_Y

        right = settings.MAX_X - w + settings.CELL_SIZE
        down = settings.MAX_Y - h + settings.CELL_SIZE

        # True if inside the girds boundary.
        if left <= x <= right and up <= y <= down:
            return True

        return False

    def calc_size(self, matrix):
        """Calculate the patterns size."""

        w, h = len(matrix[0]), len(matrix)
        width, height = w * settings.CELL_SIZE, h * settings.CELL_SIZE

        return width, height

    def preview(self, name, pos):
        matrix = self.pattern[name]
        x, y = position = calc_pos(pos)

        rects = []

        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col]:
                    rects.append(pygame.Rect(x, y, 10, 10))
                else:
                    pass
                x += settings.CELL_SIZE
            x = position[0]
            y += settings.CELL_SIZE

        if not self.is_inside_grid(position, matrix):
            return False, rects

        return True, rects

    def paste(self, pos, name):
        """Paste any predefined patterns on the grid."""

        matrix = self.pattern[name]
        x, y = position = calc_pos(pos)

        if self.is_inside_grid(position, matrix):
            for row in range(len(matrix)):
                for col in range(len(matrix[row])):
                    if matrix[row][col]:
                        self.cell[(x, y)] = 1
                        self.cell_sprite[(x, y)] = Cell((x, y))
                    else:
                        self.cell[(x, y)] = 0
                        # Delete cell sprite if there is one.
                        try:
                            del self.cell_sprite[(x, y)]
                        except KeyError:
                            pass
                    x += settings.CELL_SIZE
                x = position[0]
                y += settings.CELL_SIZE
