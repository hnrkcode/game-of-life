import itertools

from gameoflife.settings import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    BOARD_X_POS,
    BOARD_Y_POS,
    CELL_SIZE,
    LEFT_CLICK,
    MAX_X,
    MAX_Y,
    MIN_X,
    MIN_Y,
    RIGHT_CLICK,
)

from .cell import Cell


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


class Grid:
    """The 2D grid where the magic happens."""

    def __init__(self):
        self.cell = self.generate()
        self.cell_sprite = {}
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
        self.cell = self.generate()
        self.cell_sprite = {}
        self.deaths = 0
        self.generation = 0

    def update_deaths(self):
        """Keeps track of how many cells that has died."""

        self.deaths += 1

    def update(self):
        """Update the cells on the grid for the next generation."""

        births, deaths = self.life_algorithm()

        if births:
            for cell in births:
                self.cell[cell] = 1
        if deaths:
            for cell in deaths:
                self.cell[cell] = 0
                self.update_deaths()

        self.generation += 1

    def change_status(self, pos, button):
        """Point out cells on the screen with the mouse"""

        x, y = key = calc_pos(pos)

        # Prevent crashes if user clicks outside the grid.
        if MIN_X <= x <= MAX_X and MIN_Y <= y <= MAX_Y:
            if button == LEFT_CLICK and self.cell[key] == 0:
                self.cell[key] = 1
                self.cell_sprite[key] = Cell(key)
            elif button == RIGHT_CLICK and self.cell[key] == 1:
                self.cell[key] = 0
                del self.cell_sprite[key]

    def generate(self):
        """Generate list that represent the cells in the grid."""

        grid = {}

        x = BOARD_X_POS
        y = BOARD_Y_POS

        for w in range(BOARD_WIDTH):
            for h in range(BOARD_HEIGHT):
                # Positions are the keys to the values.
                key = (x, y)
                grid[key] = 0
                y += CELL_SIZE
            y = BOARD_Y_POS
            x += CELL_SIZE

        return grid

    def life_algorithm(self):
        """Conway's game of life algorithm.

        1. Living cells with fewer than two live neighbors dies.
        2. Living cells with two or three live neighbors survives.
        3. Living cells with more than three neighbors dies.
        4. Dead cells with three living neighbor cells becomes a living cell.
        """

        birth, death = [], []

        for key, value in self.cell.items():
            neighbors = self.count_neighbors(key)

            if self.cell[key] == 1:
                # Dies if under poplulated or overpopulated.
                if neighbors < 2 or neighbors > 3:
                    death.append(key)
                    del self.cell_sprite[key]
                # Cells that survives.
                if neighbors == 2 or neighbors == 3:
                    self.cell_sprite[key].next_gen()

            if self.cell[key] == 0:
                # A new cell are born.
                if neighbors == 3:
                    birth.append(key)
                    self.cell_sprite[key] = Cell(key)

        return birth, death

    def count_neighbors(self, pos):
        """Returns number of alive neighbors."""

        x, y = pos
        neighbors = 0

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

        # Count live neighbors
        for _x, _y in nlist:
            if self.cell[(_x, _y)] == 1:
                neighbors += 1

        return neighbors
