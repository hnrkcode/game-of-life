from gameoflife import settings
from gameoflife.board.grid import Grid

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

        w, h = self.calc_size(matrix)
        x, y = pos

        left = settings.MIN_X
        right = settings.MAX_X - w
        up = settings.MIN_Y
        down = settings.MAX_Y - h

        # True if inside the girds boundary.
        if left <= x <= right and up <= y <= down:
            return True

        return False

    def calc_size(self, matrix):
        """Calculate the patterns size."""

        w, h = len(matrix[0]), len(matrix)
        width, height = w * settings.CELL, h * settings.CELL

        return width, height

    def paste(self, pos, name):
        """Paste any predefined patterns on the grid."""

        matrix = self.pattern[name]
        position = self.calc_pos(pos)
        x, y = position

        if self.is_inside_grid(position, matrix):
            for row in range(len(matrix)):
                for col in range(len(matrix[row])):
                    if matrix[row][col]:
                        self.cells[(x, y)].custom_state(True)
                        self.update_living_cell(True)
                    else:
                        self.cells[(x, y)].custom_state(False)
                    x += settings.CELL
                x = position[0]
                y += settings.CELL
