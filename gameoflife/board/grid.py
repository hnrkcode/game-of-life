import copy
from collections import Counter
from typing import TypedDict

from .cell import Cell

BIRTH_NEIGHBORS = 3
SURVIVE_NEIGHBORS = (2, 3)


class Neighbors(TypedDict):
    alive: int
    dead: list[tuple[int, int]]


def count_neighbors(cell: Counter[tuple[int, int]], pos: tuple[int, int]) -> Neighbors:
    """Return number of alive neighbors."""
    x, y = pos
    neighbors: Neighbors = {"alive": 0, "dead": []}

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            key = (x + dx, y + dy)
            if cell[key] == 1:
                neighbors["alive"] += 1
            else:
                neighbors["dead"].append(key)

    return neighbors


class Grid:
    """The 2D grid where the magic happens."""

    def __init__(self) -> None:
        self.cell: Counter[tuple[int, int]] = Counter()
        self.cell_sprite: dict[tuple[int, int], Cell] = {}
        self.run = False
        self.deaths = 0
        self.generation = 0
        self.history: list[tuple[Counter[tuple[int, int]], dict[tuple[int, int], Cell], int]] = []
        self.direction: str = "forward"

    def start(self) -> None:
        """Start the algorithm."""
        self.run = True

    def stop(self) -> None:
        """Stop the algorithm."""
        self.run = False

    def reset(self) -> None:
        """Reset the grid."""
        self.stop()
        self.cell: Counter[tuple[int, int]] = Counter()
        self.cell_sprite: dict[tuple[int, int], Cell] = {}
        self.deaths = 0
        self.generation = 0
        self.history = []
        self.direction = "forward"

    def delete_cell(self, key: tuple[int, int]) -> None:
        """Remove cell from memory."""
        del self.cell[key]
        self.cell_sprite.pop(key, None)

    def update_deaths(self) -> None:
        """Keep track of how many cells that has died."""
        self.deaths += 1

    def step_back(self) -> bool:
        """Restore the previous generation from history. Returns False if no history."""
        if not self.history:
            return False
        self.cell, self.cell_sprite, self.deaths = self.history.pop()
        self.generation -= 1
        return True

    def step_forward(self) -> None:
        """Advance one generation forward."""
        self.update()

    def update(self) -> None:
        # Save snapshot before mutation.
        self.history.append(
            (
                copy.copy(self.cell),
                {k: copy.copy(v) for k, v in self.cell_sprite.items()},
                self.deaths,
            )
        )

        dead_neighbors: set[tuple[int, int]] = set()
        births: list[tuple[int, int]] = []
        deaths: list[tuple[int, int]] = []

        for key in self.cell_sprite:
            neighbors = count_neighbors(self.cell, key)

            # Survives to next generation.
            if neighbors["alive"] in SURVIVE_NEIGHBORS:
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
            if neighbors["alive"] == BIRTH_NEIGHBORS:
                self.cell_sprite[key] = Cell()
                births.append(key)

        if births:
            for cell in births:
                self.cell[cell] = 1
        if deaths:
            for cell in deaths:
                self.update_deaths()
                self.delete_cell(cell)

        self.generation += 1
