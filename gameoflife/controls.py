import pygame

from gameoflife import settings

BUTTON_NAMES = ("rewind", "skip_back", "play_pause", "stop", "skip_forward", "fast_forward")


class MediaControls:
    """Media control buttons rendered below the viewport."""

    def __init__(self) -> None:
        size = settings.CONTROLS_BUTTON_SIZE
        gap = settings.CONTROLS_GAP
        total_w = 6 * size + 5 * gap
        # Center horizontally within the viewport region.
        start_x = settings.BOARD_X_POS + (settings.BOARD_WIDTH_SIZE - total_w) // 2
        y = settings.CONTROLS_Y

        self.buttons: dict[str, pygame.Rect] = {}
        for i, name in enumerate(BUTTON_NAMES):
            x = start_x + i * (size + gap)
            self.buttons[name] = pygame.Rect(x, y, size, size)

    def handle_click(self, pos: tuple[int, int]) -> str | None:
        """Return the button name clicked, or None."""
        for name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                return name
        return None

    def draw(self, screen: pygame.Surface, grid_run: bool, direction: str) -> None:
        """Draw all six buttons."""
        hover_pos = pygame.mouse.get_pos()

        for name, rect in self.buttons.items():
            color = self._button_color(name, direction, rect.collidepoint(hover_pos))
            self._draw_symbol(screen, name, rect, color, grid_run)

    def _button_color(self, name: str, direction: str, hovered: bool) -> tuple[int, int, int]:
        # Highlight active direction.
        if name == "rewind" and direction == "backward":
            return settings.CONTROLS_ACTIVE_COLOR
        if name == "fast_forward" and direction == "forward":
            return settings.CONTROLS_ACTIVE_COLOR
        if hovered:
            return settings.CONTROLS_HOVER_COLOR
        return settings.CONTROLS_COLOR

    def _draw_symbol(
        self,
        screen: pygame.Surface,
        name: str,
        rect: pygame.Rect,
        color: tuple[int, int, int],
        grid_run: bool,
    ) -> None:
        s = rect.width
        # Consistent padding from rect edges.
        pad = max(2, s // 6)
        top = rect.top + pad
        bot = rect.bottom - pad
        left = rect.left + pad
        right = rect.right - pad
        h = bot - top  # usable height
        w = right - left  # usable width
        cy = rect.centery
        bar_w = max(2, s // 10)

        if name == "rewind":
            # Two left-pointing triangles, tightly packed.
            mid = left + w // 2
            # Right triangle (right half).
            pygame.draw.polygon(screen, color, [(right, top), (mid, cy), (right, bot)])
            # Left triangle (left half).
            pygame.draw.polygon(screen, color, [(mid, top), (left, cy), (mid, bot)])

        elif name == "skip_back":
            # Bar on left + left-pointing triangle.
            pygame.draw.rect(screen, color, (left, top, bar_w, h))
            tri_left = left + bar_w
            pygame.draw.polygon(screen, color, [(right, top), (tri_left, cy), (right, bot)])

        elif name == "play_pause":
            if grid_run:
                # Two vertical bars (pause).
                gap = max(2, s // 6)
                bw = max(2, (w - gap) // 2)
                pygame.draw.rect(screen, color, (left, top, bw, h))
                pygame.draw.rect(screen, color, (right - bw, top, bw, h))
            else:
                # Right-pointing triangle (play).
                pygame.draw.polygon(screen, color, [(left, top), (right, cy), (left, bot)])

        elif name == "stop":
            # Filled square.
            pygame.draw.rect(screen, color, (left, top, w, h))

        elif name == "skip_forward":
            # Right-pointing triangle + bar on right.
            tri_right = right - bar_w
            pygame.draw.polygon(screen, color, [(left, top), (tri_right, cy), (left, bot)])
            pygame.draw.rect(screen, color, (right - bar_w, top, bar_w, h))

        elif name == "fast_forward":
            # Two right-pointing triangles, tightly packed.
            mid = left + w // 2
            # Left triangle (left half).
            pygame.draw.polygon(screen, color, [(left, top), (mid, cy), (left, bot)])
            # Right triangle (right half).
            pygame.draw.polygon(screen, color, [(mid, top), (right, cy), (mid, bot)])
