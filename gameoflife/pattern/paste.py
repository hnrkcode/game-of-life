import pygame
from gameoflife import settings
from gameoflife.board.cell import Cell
from gameoflife.board.grid import Grid, calc_pos, calc_size, is_inside_grid

from .blueprint import get_patterns
from .select import PatternSelector


class PastePattern(Grid):
    """Read in predefined patterns and paste them on the grid."""

    def __init__(self):
        super().__init__()
        self.select = PatternSelector()
        self.pattern = get_patterns()

        for name in self.pattern.keys():
            self.select.append((name, self.paste))

    def set_color(self, pos, matrix):
        if not is_inside_grid(pos, matrix):
            return settings.PASTE_OFF
        return settings.PASTE_ON

    def preview(self, pos, name=None):
        """Show preview of selected pattern."""

        if not name:
            pattern_matrix = [[1]]
        else:
            pattern_matrix = self.pattern[name]

        size = settings.CELL_SIZE
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
                    pygame.draw.rect(pattern_surface, pattern_color, pattern_rect)

        return pattern_surface

    def paste(self, pos, button, name=None):
        """Paste any predefined patterns on the grid."""

        if not name:
            matrix = [[1]]
        else:
            matrix = self.pattern[name]

        x, y = position = calc_pos(pos)

        if is_inside_grid(position, matrix):
            for row in range(len(matrix)):
                for col in range(len(matrix[row])):
                    # Draw cells.
                    if button == settings.LEFT_CLICK and matrix[row][col]:
                        self.cell[(x, y)] = 1
                        self.cell_sprite[(x, y)] = Cell((x, y))

                    # Erase cells.
                    if button == settings.RIGHT_CLICK or not matrix[row][col]:
                        self.delete_cell((x, y))

                    x += settings.CELL_SIZE

                x = position[0]
                y += settings.CELL_SIZE
