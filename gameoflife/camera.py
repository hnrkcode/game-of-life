import math


class Camera:
    """Manages the viewport into an infinite world grid."""

    def __init__(
        self,
        viewport_x: int,
        viewport_y: int,
        viewport_w: int,
        viewport_h: int,
        cell_size: float = 10.0,
        min_cell_size: float = 2.0,
        max_cell_size: float = 50.0,
    ) -> None:
        self.viewport_x = viewport_x
        self.viewport_y = viewport_y
        self.viewport_w = viewport_w
        self.viewport_h = viewport_h
        self.cell_size = cell_size
        self.min_cell_size = min_cell_size
        self.max_cell_size = max_cell_size
        # World coordinate at the center of the viewport.
        self.world_center_x: float = 0.0
        self.world_center_y: float = 0.0

    def world_to_screen(self, wx: int, wy: int) -> tuple[float, float]:
        """Convert a world cell coordinate to screen pixel position (top-left of cell)."""
        sx = self.viewport_x + self.viewport_w / 2 + (wx - self.world_center_x) * self.cell_size
        sy = self.viewport_y + self.viewport_h / 2 + (wy - self.world_center_y) * self.cell_size
        return sx, sy

    def screen_to_world(self, sx: int, sy: int) -> tuple[int, int]:
        """Convert a screen pixel position to the world cell coordinate it falls within."""
        wx = math.floor((sx - self.viewport_x - self.viewport_w / 2) / self.cell_size + self.world_center_x)
        wy = math.floor((sy - self.viewport_y - self.viewport_h / 2) / self.cell_size + self.world_center_y)
        return wx, wy

    def get_visible_bounds(self) -> tuple[int, int, int, int]:
        """Return (min_wx, min_wy, max_wx, max_wy) of visible world cells."""
        min_wx = math.floor(self.world_center_x - self.viewport_w / (2 * self.cell_size))
        min_wy = math.floor(self.world_center_y - self.viewport_h / (2 * self.cell_size))
        max_wx = math.ceil(self.world_center_x + self.viewport_w / (2 * self.cell_size))
        max_wy = math.ceil(self.world_center_y + self.viewport_h / (2 * self.cell_size))
        return min_wx, min_wy, max_wx, max_wy

    def zoom(self, factor: float, anchor_sx: int, anchor_sy: int) -> None:
        """Zoom in/out keeping the world point under the anchor screen position fixed."""
        # World coord under cursor before zoom.
        wx_before = (anchor_sx - self.viewport_x - self.viewport_w / 2) / self.cell_size + self.world_center_x
        wy_before = (anchor_sy - self.viewport_y - self.viewport_h / 2) / self.cell_size + self.world_center_y

        self.cell_size = max(self.min_cell_size, min(self.max_cell_size, self.cell_size * factor))

        # Adjust center so the same world point is still under the cursor.
        self.world_center_x = wx_before - (anchor_sx - self.viewport_x - self.viewport_w / 2) / self.cell_size
        self.world_center_y = wy_before - (anchor_sy - self.viewport_y - self.viewport_h / 2) / self.cell_size

    def pan(self, dx_pixels: int, dy_pixels: int) -> None:
        """Pan the camera by a screen-space pixel delta."""
        self.world_center_x -= dx_pixels / self.cell_size
        self.world_center_y -= dy_pixels / self.cell_size

    def is_in_viewport(self, sx: int, sy: int) -> bool:
        """Check if a screen pixel is within the viewport area."""
        return self.viewport_x <= sx < self.viewport_x + self.viewport_w and self.viewport_y <= sy < self.viewport_y + self.viewport_h
