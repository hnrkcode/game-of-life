import math

from gameoflife import settings
from gameoflife.pattern.select import PatternSelector
from gameoflife.util.text import InfoText


class ScrollMenu:
    def __init__(self) -> None:
        self.num = 5

    def setup(self, patterns: PatternSelector) -> tuple[list[str], list[str]]:
        """Return adjacent patterns."""
        prev_value = [patterns.before_current(i) for i in range(1, self.num + 1)]
        next_value = [patterns.after_current(i) for i in range(1, self.num + 1)]

        return next_value, prev_value

    def text_color(self, n: int) -> tuple[int, int, int]:
        """Return color for none active menu object."""
        return int(150 / n), int(150 / n), int(150 / n)

    def format(
        self,
        header_text: str,
        active: str,
        adjacent: tuple[list[str], list[str]],
        header_size: int = 25,
        item_size: int = 15,
    ) -> list[InfoText]:
        """Return list with formated menu objects."""
        next_value, prev_value = [], []
        menu_header = [InfoText(header_text, header_size)]
        active_pattern = [InfoText(active, item_size, color=settings.ACTIVE)]

        for i in range(self.num):
            for j in range(2):
                item_name = adjacent[j][i]
                color = self.text_color(i + 1)

                if j == 0:
                    next_pattern = InfoText(item_name, item_size, color=color)
                    next_value.insert(0, next_pattern)
                else:
                    prev_pattern = InfoText(item_name, item_size, color=color)
                    prev_value.append(prev_pattern)

        menu = menu_header + next_value + active_pattern + prev_value

        return menu  # noqa: RET504

    def update(self, display: list[InfoText], menu: tuple[list[str], list[str]], active: str, start: int, end: int) -> None:
        """Update menu before redraw it on the screen."""
        next_value = self.num - 1
        prev_value = 0
        mid = end - math.ceil((end - start) / 2)

        for i in range(start, end):
            if start <= i < mid:
                display[i].update(menu[0][next_value])
                next_value -= 1
            elif i == mid:
                display[i].update(active)
            elif mid < i < end:
                display[i].update(menu[1][prev_value])
                prev_value += 1
