import itertools

from gameoflife import settings

from .cell import Cell


class Grid:
    """The 2D grid where the magic happens."""

    def __init__(self):
        self.cells = self.generate_grid()
        self.living = 0
        self.deaths = 0
        self.generation = 0
        self.run = False

    def start(self):
        """Start the algorithm."""
        self.run = True

    def stop(self):
        """Stop the algorithm."""
        self.run = False

    def reset(self):
        """Reset the grid."""
        self.stop()
        self.living = 0
        self.deaths = 0
        self.generation = 0
        self.cells = self.generate_grid()

    def update_living_cell(self, cell):
        """Keep track of how many cells that are currently alive."""
        if cell:
            self.living += 1
        else:
            self.living -= 1

    def update_deaths(self):
        """Keeps track of how many cells that has died."""
        self.deaths += 1

    def update(self):
        """Update the cells on the grid for the next generation."""
        births, deaths = self.life_algorithm()

        if births:
            for cell in births:
                self.cells[cell].change_state()
                self.update_living_cell(True)
        if deaths:
            for cell in deaths:
                self.cells[cell].change_state()
                self.update_living_cell(False)
                self.update_deaths()

        self.generation += 1

    def calc_pos(self, pos):
        """Calculate the key for the current mouse position."""
        x, y = pos
        # Calculate the acceptable interval the exact coordinate has.
        low_x = (x // settings.CELL) * settings.CELL
        high_x = low_x + (settings.CELL - 1)
        low_y = (y // settings.CELL) * settings.CELL
        high_y = low_y + (settings.CELL - 1)

        # Find the key that should get the value.
        if low_x <= x <= high_x and low_y <= y <= high_y:
            # Calculate the exact key.
            x = x // settings.CELL * settings.CELL
            y = y // settings.CELL * settings.CELL
            key = (x, y)
            return key

    def change_status(self, pos, button):
        """Point out cells on the screen with the mouse"""
        x, y = key = self.calc_pos(pos)
        min_x, max_x = settings.MIN_X, settings.MAX_X
        min_y, max_y = settings.MIN_Y, settings.MAX_Y

        # Prevent crashes if user clicks outside the grid.
        if min_x <= x <= max_x and min_y <= y <= max_y:
            if button == settings.LEFT_CLICK:
                if not self.cells[key].alive:
                    self.cells[key].change_state()
                    self.update_living_cell(True)
            elif button == settings.RIGHT_CLICK:
                if self.cells[key].alive:
                    self.cells[key].change_state()
                    self.update_living_cell(False)

    def generate_grid(self):
        """Create all the cells"""

        grid = {}

        x = settings.BOARD_X_POS
        y = settings.BOARD_Y_POS

        for w in range(settings.BOARD_WIDTH):
            for h in range(settings.BOARD_HEIGHT):
                key = (x, y)  # Positions are the keys to the values.
                grid[key] = Cell([x, y])
                y += settings.CELL
            y = settings.BOARD_Y_POS
            x += settings.CELL

        return grid

    def life_algorithm(self):
        """Conway's game of life algorithm.

        1. Living cells with fewer than two live neighbors dies.
        2. Living cells with two or three live neighbors survives.
        3. Living cells with more than three neighbors dies.
        4. Dead cells with three living neighbor cells becomes a living cell.
        """
        birth, death = [], []
        for key, value in self.cells.items():
            neighbors = self.count_neighbors(key)
            if self.cells[key].alive:
                # Dies if under poplulated or overpopulated.
                if neighbors < 2 or neighbors > 3:
                    death.append(key)
                    self.cells[key].reset()
                # Cells that survives.
                if neighbors == 2 or neighbors == 3:
                    self.cells[key].next_gen()

            if not self.cells[key].alive:
                # A new cell are born.
                if neighbors == 3:
                    birth.append(key)

        return birth, death

    def count_neighbors(self, pos):
        """Returns number of alive neighbors."""
        x, y = pos
        neighbors = 0
        size = settings.CELL
        min_x, max_x = settings.MIN_X, settings.MAX_X
        min_y, max_y = settings.MIN_Y, settings.MAX_Y
        # Calculate positions of all neighbors.
        nlist = list(
            itertools.product(
                range(x - size, x + size * 2, size),
                range(y - size, y + size * 2, size),
            )
        )
        # Remove the cell that we checked neighbors for from the list.
        nlist.remove((x, y))
        # Fix calculated positions that are outside the border.
        new_nlist = []
        for _x, _y in nlist:
            tmpx, tmpy = _x, _y
            if _x < min_x or _x > max_x or _y < min_y or _y > max_y:
                if _x < min_x:
                    tmpx = max_x
                elif _x > max_x:
                    tmpx = min_x
                if _y < min_y:
                    tmpy = max_y
                elif _y > max_y:
                    tmpy = min_y
            new_nlist.append((tmpx, tmpy))
        nlist = new_nlist
        # Count live neighbors
        for _x, _y in nlist:
            if self.cells[_x, _y].alive:
                neighbors += 1

        return neighbors
