import math

from gameoflife import settings
from gameoflife.util.text import InfoText


class ScrollMenu:
    def __init__(self):
        self.num = 5

    def setup(self, patterns):
        """Return adjacent patterns."""

        prev = [patterns.before_current(i) for i in range(1, self.num + 1)]
        next = [patterns.after_current(i) for i in range(1, self.num + 1)]

        return next, prev

    def text_color(self, n):
        """Return color for none active menu object."""

        return int(150 / n), int(150 / n), int(150 / n)

    def format(self, header_text, active, adjacent, header_size=25, item_size=15):
        """Return list with formated menu objects."""

        next, prev = [], []
        menu_header = [InfoText(header_text, header_size)]
        active_pattern = [InfoText(active, item_size, color=settings.ACTIVE)]

        for i in range(self.num):
            for j in range(2):
                item_name = adjacent[j][i]
                color = self.text_color(i + 1)

                if j == 0:
                    next_pattern = InfoText(item_name, item_size, color=color)
                    next.insert(0, next_pattern)
                else:
                    prev_pattern = InfoText(item_name, item_size, color=color)
                    prev.append(prev_pattern)

        menu = menu_header + next + active_pattern + prev

        return menu

    def update(self, display, menu, active, start, end):
        """Update menu before redraw it on the screen."""

        next = self.num - 1
        prev = 0
        mid = end - math.ceil((end - start) / 2)

        for i in range(start, end):
            if start <= i < mid:
                display[i].update(menu[0][next])
                next -= 1
            elif i == mid:
                display[i].update(active)
            elif mid < i < end:
                display[i].update(menu[1][prev])
                prev += 1
