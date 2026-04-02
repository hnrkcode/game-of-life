import pygame

from gameoflife import settings
from gameoflife.board.cell import Cell
from gameoflife.board.grid import Grid

from .blueprint import get_patterns
from .select import PatternSelector


def get_pattern_matrix(patterns: dict, name: str | None) -> list[list[int]]:
    return patterns[name] if name else [[1]]


class PastePattern(Grid):
    """Read in predefined patterns and paste them on the grid."""

    def __init__(self) -> None:
        super().__init__()
        self.select = PatternSelector()
        self.pattern = get_patterns()

        for name in self.pattern:
            self.select.append((name, self.paste))

    def preview(self, name: str | None = None, cell_size: float = 10.0) -> pygame.Surface:
        """Show preview of selected pattern."""
        pattern_matrix = get_pattern_matrix(self.pattern, name)

        size = max(1, int(cell_size))
        w, h = len(pattern_matrix[0]) * size, len(pattern_matrix) * size
        pattern_surface = pygame.Surface((w, h))
        pattern_surface.set_colorkey((0, 0, 0))
        pattern_surface.set_alpha(50)

        # Draw pattern to a surface with the same size.
        for row in range(len(pattern_matrix)):
            for col in range(len(pattern_matrix[row])):
                if pattern_matrix[row][col]:
                    xy_coords = [col * size, row * size]
                    wh_size = [size] * 2
                    pattern_rect = pygame.Rect(xy_coords, wh_size)
                    pygame.draw.rect(pattern_surface, settings.PASTE_ON, pattern_rect)

        return pattern_surface

    def paste(self, world_pos: tuple[int, int], button: tuple[bool, bool, bool], name: str | None = None) -> None:
        """Paste any predefined patterns on the grid."""
        matrix = get_pattern_matrix(self.pattern, name)
        wx, wy = world_pos

        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                key = (wx + col, wy + row)

                # Draw cells.
                if button == settings.LEFT_CLICK and matrix[row][col]:
                    self.cell[key] = 1
                    self.cell_sprite[key] = Cell()

                # Erase cells.
                if (button == settings.RIGHT_CLICK or not matrix[row][col]) and key in self.cell:
                    self.delete_cell(key)
