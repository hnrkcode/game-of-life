import pygame

from gameoflife import settings
from gameoflife.board.cell import Cell
from gameoflife.board.grid import Grid

from .blueprint import get_patterns
from .select import PatternSelector
from .transform import flip_horizontal, flip_vertical, rotate_ccw, rotate_cw


def get_pattern_matrix(patterns: dict, name: str | None) -> list[list[int]]:
    return patterns[name] if name else [[1]]


class PastePattern(Grid):
    """Read in predefined patterns and paste them on the grid."""

    def __init__(self) -> None:
        super().__init__()
        self.select = PatternSelector()
        self.pattern = get_patterns()
        self._transformed: list[list[int]] | None = None

        for name in self.pattern:
            self.select.append((name, self.paste))

    def get_effective_matrix(self, name: str | None) -> list[list[int]]:
        """Return the transformed matrix if set, otherwise the raw pattern."""
        if self._transformed is not None:
            return self._transformed
        return get_pattern_matrix(self.pattern, name)

    def reset_transform(self) -> None:
        """Clear any applied transformation."""
        self._transformed = None

    def rotate_pattern_cw(self, name: str | None) -> None:
        """Rotate the current pattern 90° clockwise."""
        self._transformed = rotate_cw(self.get_effective_matrix(name))

    def rotate_pattern_ccw(self, name: str | None) -> None:
        """Rotate the current pattern 90° counter-clockwise."""
        self._transformed = rotate_ccw(self.get_effective_matrix(name))

    def flip_pattern_h(self, name: str | None) -> None:
        """Flip the current pattern horizontally (left-right)."""
        self._transformed = flip_horizontal(self.get_effective_matrix(name))

    def flip_pattern_v(self, name: str | None) -> None:
        """Flip the current pattern vertically (top-bottom)."""
        self._transformed = flip_vertical(self.get_effective_matrix(name))

    def preview(
        self,
        name: str | None = None,
        cell_size: float = 10.0,
        color: tuple[int, int, int] = settings.PASTE_ON,
    ) -> pygame.Surface:
        """Show preview of selected pattern."""
        pattern_matrix = self.get_effective_matrix(name)

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
                    pygame.draw.rect(pattern_surface, color, pattern_rect)

        return pattern_surface

    def paste(self, world_pos: tuple[int, int], button: tuple[bool, bool, bool], name: str | None = None) -> None:
        """Paste any predefined patterns on the grid."""
        matrix = self.get_effective_matrix(name)
        rows = len(matrix)
        cols = len(matrix[0])
        wx, wy = world_pos
        # Center the pattern on the target position.
        ox = wx - cols // 2
        oy = wy - rows // 2

        for row in range(rows):
            for col in range(cols):
                key = (ox + col, oy + row)

                # Draw cells.
                if button == settings.LEFT_CLICK and matrix[row][col]:
                    self.cell[key] = 1
                    self.cell_sprite[key] = Cell()

                # Erase cells.
                if (button == settings.RIGHT_CLICK or not matrix[row][col]) and key in self.cell:
                    self.delete_cell(key)
