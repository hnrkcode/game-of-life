import itertools
from collections import Counter

from gameoflife.settings import (
    CELL_SIZE,
    MAX_X,
    MAX_Y,
    MIN_X,
    MIN_Y,
)

from .cell import Cell


def is_inside_grid(pos, matrix):
    """Make sure the pattern is pasted inside the grids boundary."""

    x, y = pos
    w, h = calc_size(matrix)

    left = MIN_X
    up = MIN_Y

    right = MAX_X - w + CELL_SIZE
    down = MAX_Y - h + CELL_SIZE

    # True if inside the girds boundary.
    if left <= x <= right and up <= y <= down:
        return True

    return False


def calc_size(matrix):
    """Calculate the patterns size."""

    w, h = len(matrix[0]), len(matrix)
    width, height = w * CELL_SIZE, h * CELL_SIZE

    return width, height


def calc_pos(pos):
    """Calculate the key for the current mouse position."""

    x, y = pos

    # Calculate the acceptable interval the exact coordinate has.
    low_x = (x // CELL_SIZE) * CELL_SIZE
    high_x = low_x + (CELL_SIZE - 1)
    low_y = (y // CELL_SIZE) * CELL_SIZE
    high_y = low_y + (CELL_SIZE - 1)

    # Find the key that should get the value.
    if low_x <= x <= high_x and low_y <= y <= high_y:
        # Calculate the exact key.
        x = x // CELL_SIZE * CELL_SIZE
        y = y // CELL_SIZE * CELL_SIZE
        key = (x, y)

        return key


def count_neighbors(cell, pos):
    """Returns number of alive neighbors."""

    x, y = pos
    neighbors = {"alive": 0, "dead": []}

    # Calculate positions of all neighbors.
    nlist = list(
        itertools.product(
            range(x - CELL_SIZE, x + CELL_SIZE * 2, CELL_SIZE),
            range(y - CELL_SIZE, y + CELL_SIZE * 2, CELL_SIZE),
        )
    )

    # Remove the cell that we checked neighbors for from the list.
    nlist.remove((x, y))

    # Fix calculated positions that are outside the border.
    new_nlist = []
    for _x, _y in nlist:
        tmpx, tmpy = _x, _y
        if _x < MIN_X or _x > MAX_X or _y < MIN_Y or _y > MAX_Y:
            if _x < MIN_X:
                tmpx = MAX_X
            elif _x > MAX_X:
                tmpx = MIN_X
            if _y < MIN_Y:
                tmpy = MAX_Y
            elif _y > MAX_Y:
                tmpy = MIN_Y
        new_nlist.append((tmpx, tmpy))
    nlist = new_nlist

    for key in nlist:
        if cell[key] == 1:
            neighbors["alive"] += 1
        else:
            neighbors["dead"].append(key)

    return neighbors


class Grid:
    """The 2D grid where the magic happens."""

    def __init__(self):
        self.cell = Counter()
        self.cell_sprite = Counter()
        self.run = False
        self.deaths = 0
        self.generation = 0

    def start(self):
        """Start the algorithm."""

        self.run = True

    def stop(self):
        """Stop the algorithm."""

        self.run = False

    def reset(self):
        """Reset the grid."""

        self.stop()
        self.cell = Counter()
        self.cell_sprite = Counter()
        self.deaths = 0
        self.generation = 0

    def delete_cell(self, key):
        """Remove cell from memory."""

        del self.cell[key]
        del self.cell_sprite[key]

    def update_deaths(self):
        """Keeps track of how many cells that has died."""

        self.deaths += 1

    def update(self):
        dead_neighbors = set()
        births, deaths = [], []

        for key, _ in self.cell_sprite.items():
            neighbors = count_neighbors(self.cell, key)

            # Survives to next generation.
            if neighbors["alive"] == 2 or neighbors["alive"] == 3:
                self.cell_sprite[key].next_gen()
                births.append(key)

            # Doesn't survive the current generation.
            else:
                deaths.append(key)

            # Cache dead neighboring cells.
            for dead_cell in neighbors["dead"]:
                dead_neighbors.add(dead_cell)

        # Check cached dead cells to see if they have enough live cells to be born next generation.
        for key in dead_neighbors:
            neighbors = count_neighbors(self.cell, key)

            # New cells that gets born next generation.
            if neighbors["alive"] == 3:
                self.cell_sprite[key] = Cell(key)
                births.append(key)

        if births:
            for cell in births:
                self.cell[cell] = 1
        if deaths:
            for cell in deaths:
                self.update_deaths()
                self.delete_cell(cell)

        self.generation += 1
