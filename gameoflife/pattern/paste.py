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

    def set_color(self, pos, matrix):
        if not self.is_inside_grid(pos, matrix):
            return settings.PASTE_OFF
        return settings.PASTE_ON

    def preview(self, name, pos):
        """Show preview of selected pattern."""

        size = settings.CELL_SIZE
        pattern_matrix = self.pattern[name]
        w, h = len(pattern_matrix[0]) * size, len(pattern_matrix) * size
        pattern_surface = pygame.Surface((w, h))
        pattern_surface.set_colorkey((0, 0, 0))
        pattern_surface.set_alpha(50)
        pattern_color = self.set_color(pos, pattern_matrix)

        # Draw pattern to a surface with the same size.
        for row in range(len(pattern_matrix)):
            for col in range(len(pattern_matrix[row])):
                # Draw only parts of the pattern that is visible.
                if pattern_matrix[row][col]:
                    xy_coords = [col * size, row * size]
                    wh_size = [size] * 2
                    pattern_rect = pygame.Rect(xy_coords, wh_size)
                    pygame.draw.rect(
                        pattern_surface, pattern_color, pattern_rect
                    )

        return pattern_surface

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
