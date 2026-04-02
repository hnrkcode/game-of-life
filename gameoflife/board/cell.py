import math

from gameoflife import settings

GEN1_RANGE = (1, 5)
GEN2_RANGE = (5, 10)
GEN3_RANGE = (10, 50)
GEN4_RANGE = (50, 100)
GEN5_RANGE = (100, math.inf)


class Cell:
    def __init__(self) -> None:
        self.color = settings.ALIVE
        self.generation = 0

    def next_gen(self) -> None:
        """Update the generations the cell has existed and colorize it."""
        self.generation += 1
        if GEN1_RANGE[0] < self.generation <= GEN1_RANGE[1]:
            self.color = settings.GEN1
        elif GEN2_RANGE[0] < self.generation <= GEN2_RANGE[1]:
            self.color = settings.GEN2
        elif GEN3_RANGE[0] < self.generation <= GEN3_RANGE[1]:
            self.color = settings.GEN3
        elif GEN4_RANGE[0] < self.generation <= GEN4_RANGE[1]:
            self.color = settings.GEN4
        elif GEN5_RANGE[0] < self.generation <= GEN5_RANGE[1]:
            self.color = settings.GEN5
