import patterns
import settings
from grid import Grid
from selector import PatternSelector

class Pattern(Grid):

    def __init__(self):
        super().__init__()

        self.select = PatternSelector()
        self.select.append(("Blinker", self.paste_pattern))
        self.select.append(("Pulsar", self.paste_pattern))
        self.select.append(("Pinwheel", self.paste_pattern))
        self.select.append(("Octagon 2", self.paste_pattern))
        self.select.append(("Glider", self.paste_pattern))
        self.select.append(("LWSS", self.paste_pattern))
        self.select.append(("25P3H1V0.1", self.paste_pattern))
        self.select.append(("Weekender", self.paste_pattern))
        self.select.append(("Gosperglidergun", self.paste_pattern))
        self.select.append(("Garden of Eden", self.paste_pattern))

    def is_inside_grid(self, pos, matrix):
        """Make sure the pattern is pasted inside the grids boundary."""
        w, h = self.calc_size(matrix)
        x, y = pos

        left = settings.MIN_X
        right = settings.MAX_X-w
        up = settings.MIN_Y
        down = settings.MAX_Y-h

        # True if inside the girds boundary.
        if left <= x <= right and up <= y <= down:
            return True

        return False

    def calc_size(self, matrix):
        """Calculate the patterns size."""
        width, height = len(matrix[0]), len(matrix)
        width, height = width*settings.CELL, height*settings.CELL

        return width, height

    def paste_pattern(self, pos, name):
        """Paste any predefined patterns on the grid."""
        matrix = patterns.pattern[name]
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
