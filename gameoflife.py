#!/usr/bin/env python3.6

import os
import pygame
import settings
from pygame import locals
from patterns import pattern
from selector import PatternSelector


class Cell(pygame.sprite.Sprite):
    """Individual cells on the grid."""

    def __init__(self, pos):
        super().__init__()
        self.color = settings.DEAD
        self.image = pygame.Surface([settings.CELL, settings.CELL])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.alive = False
        self.generation = 0

    def custom_state(self, state):
        """Switch to the chosen state."""
        self.alive = state
        if self.alive:
            self.color = settings.ALIVE
            self.image.fill(self.color)
        else:
            self.color = settings.DEAD
            self.image.fill(self.color)

    def change_state(self):
        """Switch to the opposite state."""
        if self.alive:
            self.alive = False
            self.color = settings.DEAD
            self.image.fill(self.color)
        else:
            self.alive = True
            self.color = settings.ALIVE
            self.image.fill(self.color)

    def next_gen(self):
        """Update the generations the cell has existed and colorize it."""
        if self.alive:
            self.generation += 1
            if 1 < self.generation <= 5:
                self.color = settings.GEN1
                self.image.fill(self.color)
            elif 5 < self.generation <= 10:
                self.color = settings.GEN2
                self.image.fill(self.color)
            elif 10 < self.generation <= 50:
                self.color = settings.GEN3
                self.image.fill(self.color)
            elif 50 < self.generation <= 100:
                self.color = settings.GEN4
                self.image.fill(self.color)
            elif 100 < self.generation:
                self.color = settings.GEN5
                self.image.fill(self.color)
        else:
            self.reset()

    def reset(self):
        """Set the generation back to zero if cell has died."""
        self.generation = 0
        self.color = settings.DEAD
        self.image.fill(self.color)


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
        low_x = ((x // settings.CELL) * settings.CELL)
        high_x = low_x + (settings.CELL - 1)
        low_y = ((y // settings.CELL) * settings.CELL)
        high_y = low_y + (settings.CELL - 1)

        # Find the key that should get the value.
        if (low_x <= x <= high_x and low_y <= y <= high_y):
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

        # TODO: Fix this mess later... even though it works.
        # Cells inside the border except the cells next to the border.
        if min_x < x < max_x and min_y < y < max_y:
            # Left
            if self.cells[x-size, y].alive:
                neighbors += 1
            # Right
            if self.cells[x+size, y].alive:
                neighbors += 1
            # Up
            if self.cells[x, y-size].alive:
                neighbors += 1
            # Down
            if self.cells[x, y+size].alive:
                neighbors += 1
            # Leftup
            if self.cells[x-size, y-size].alive:
                neighbors += 1
            # Leftdown
            if self.cells[x-size, y+size].alive:
                neighbors += 1
            # Rightup
            if self.cells[x+size, y-size].alive:
                neighbors += 1
            # Rightdown
            if self.cells[x+size, y+size].alive:
                neighbors += 1

        # Every cell on the edge of the border.
        elif x == min_x or x == max_x or y == min_y or y == max_y:

            # Left up down corners
            if x == min_x and y == min_y:  # Upper left corner.
                # Special case.
                # Left
                if self.cells[max_x, y].alive:
                    neighbors += 1
                # Up
                if self.cells[x, max_y].alive:
                    neighbors += 1
                # Leftup
                if self.cells[max_x, max_y].alive:
                    neighbors += 1
                # Leftdown
                if self.cells[max_x, min_y].alive:
                    neighbors += 1
                # Rightup
                if self.cells[min_x+size, max_y].alive:
                    neighbors += 1
                # Normal case.
                # Right
                if self.cells[x+size, y].alive:
                    neighbors += 1
                # Down
                if self.cells[x, y+size].alive:
                    neighbors += 1
                # Rightdown
                if self.cells[x+size, y+size].alive:
                    neighbors += 1

            if x == min_x and y == max_y:  # Bottom left corner.
                # Special case.
                # Left
                if self.cells[max_x, max_y].alive:
                    neighbors += 1
                # Leftup
                if self.cells[max_x, max_y-size].alive:
                    neighbors += 1
                # Leftdown
                if self.cells[max_x, min_y].alive:
                    neighbors += 1
                # Down
                if self.cells[min_x, min_y].alive:
                    neighbors += 1
                # Normal cases
                # Up
                if self.cells[min_x, max_y-size].alive:
                    neighbors += 1
                # Rightup
                if self.cells[min_x+size, max_y].alive:
                    neighbors += 1
                # Right
                if self.cells[x+size, y].alive:
                    neighbors += 1
                # Rightdown
                if self.cells[min_x+size, min_y].alive:
                    neighbors += 1

            # Right up corners
            if x == max_x and y == min_y:  # Upper right corner.
                # Special cases.
                # Up
                if self.cells[max_x, max_y].alive:
                    neighbors += 1
                # Leftup
                if self.cells[x-size, max_y].alive:
                    neighbors += 1
                # Rightup
                if self.cells[min_x, max_y].alive:
                    neighbors += 1
                # Rightdown
                if self.cells[min_x, y+size].alive:
                    neighbors += 1
                # Right
                if self.cells[min_x, y].alive:
                    neighbors += 1
                # Normal cases
                # Left
                if self.cells[x-size, y].alive:
                    neighbors += 1
                # Down
                if self.cells[x, y+size].alive:
                    neighbors += 1
                # Leftdown
                if self.cells[x-size, y+size].alive:
                    neighbors += 1

            if x == max_x and y == max_y:  # Bottom right corner.
                # Left
                if self.cells[x-size, y].alive:
                    neighbors += 1
                # Right
                if self.cells[min_x, y].alive:
                    neighbors += 1
                # Up
                if self.cells[x, y-size].alive:
                    neighbors += 1
                # Down
                if self.cells[x, min_y].alive:
                    neighbors += 1
                # Leftup
                if self.cells[x-size, y-size].alive:
                    neighbors += 1
                # Leftdown
                if self.cells[max_x-size, min_y].alive:
                    neighbors += 1
                # Rightup
                if self.cells[min_x, max_y-size].alive:
                    neighbors += 1
                # Rightdown
                if self.cells[min_x, min_y].alive:
                    neighbors += 1

            # Between the four corners.
            # Between upper corners.
            if min_x < x < max_x and y == min_y:
                # Left
                if self.cells[x-size, y].alive:
                    neighbors += 1
                # Right
                if self.cells[x+size, y].alive:
                    neighbors += 1
                # Up
                if self.cells[x, max_y].alive:
                    neighbors += 1
                # Down
                if self.cells[x, y+size].alive:
                    neighbors += 1
                # Leftup
                if self.cells[x-size, max_y].alive:
                    neighbors += 1
                # Leftdown
                if self.cells[x-size, y+size].alive:
                    neighbors += 1
                # Rightup
                if self.cells[x+size, max_y].alive:
                    neighbors += 1
                # Rightdown
                if self.cells[x+size, y+size].alive:
                    neighbors += 1

            # Between bottom corners.
            if min_x < x < max_x and y == max_y:
                # Left
                if self.cells[x-size, y].alive:
                    neighbors += 1
                # Right
                if self.cells[x+size, y].alive:
                    neighbors += 1
                # Up
                if self.cells[x, y-size].alive:
                    neighbors += 1
                # Down
                if self.cells[x, min_y].alive:
                    neighbors += 1
                # Leftup
                if self.cells[x-size, y-size].alive:
                    neighbors += 1
                # Leftdown
                if self.cells[x-size, min_y].alive:
                    neighbors += 1
                # Rightup
                if self.cells[x+size, y-size].alive:
                    neighbors += 1
                # Rightdown
                if self.cells[x+size, min_y].alive:
                    neighbors += 1

            # Between left corners.
            if x == min_x and min_y < y < max_y:
                # Left
                if self.cells[max_x, y].alive:
                    neighbors += 1
                # Right
                if self.cells[x+size, y].alive:
                    neighbors += 1
                # Up
                if self.cells[x, y-size].alive:
                    neighbors += 1
                # Down
                if self.cells[x, y+size].alive:
                    neighbors += 1
                # Leftup
                if self.cells[max_x, y-size].alive:
                    neighbors += 1
                # Leftdown
                if self.cells[max_x, y+size].alive:
                    neighbors += 1
                # Rightup
                if self.cells[x+size, y-size].alive:
                    neighbors += 1
                # Rightdown
                if self.cells[x+size, y+size].alive:
                    neighbors += 1

            # Between right corners.
            if x == max_x and min_y < y < max_y:
                # Left
                if self.cells[x-size, y].alive:
                    neighbors += 1
                # Right
                if self.cells[min_x, y].alive:
                    neighbors += 1
                # Up
                if self.cells[x, y-size].alive:
                    neighbors += 1
                # Down
                if self.cells[x, y+size].alive:
                    neighbors += 1
                # Leftup
                if self.cells[x-size, y-size].alive:
                    neighbors += 1
                # Leftdown
                if self.cells[x-size, y+size].alive:
                    neighbors += 1
                # Rightup
                if self.cells[min_x, y-size].alive:
                    neighbors += 1
                # Rightdown
                if self.cells[min_x, y+size].alive:
                    neighbors += 1

        return neighbors


class Pattern(Grid):

    def __init__(self):
        super().__init__()

        self.select = PatternSelector()
        self.select.append(("Blinker", self.paste_pattern))
        self.select.append(("Pulsar", self.paste_pattern))
        self.select.append(("Pinwheel", self.paste_pattern))
        self.select.append(("Octagon 2", self.paste_pattern))
        self.select.append(("Glider", self.paste_pattern))
        self.select.append(("LWSS", self.paste_pattern))
        self.select.append(("25P3H1V0.1", self.paste_pattern))
        self.select.append(("Weekender", self.paste_pattern))
        self.select.append(("Gosperglidergun", self.paste_pattern))
        self.select.append(("Garden of Eden", self.paste_pattern))

    def is_inside_grid(self, pos, matrix):
        """Make sure the pattern is pasted inside the grids boundary."""
        w, h = self.calc_size(matrix)
        x, y = pos

        left = settings.MIN_X
        right = settings.MAX_X-w
        up = settings.MIN_Y
        down = settings.MAX_Y-h

        # True if inside the girds boundary.
        if left <= x <= right and up <= y <= down:
            return True

        return False

    def calc_size(self, matrix):
        """Calculate the patterns size."""
        width, height = len(matrix[0]), len(matrix)
        width, height = width*settings.CELL, height*settings.CELL

        return width, height

    def paste_pattern(self, pos, name):
        """Paste any predefined patterns on the grid."""
        matrix = pattern[name]
        position = self.calc_pos(pos)
        x, y = position

        if self.is_inside_grid(position, matrix):
            for row in range(len(matrix)):
                for col in range(len(matrix[row])):
                    if matrix[row][col]:
                        self.cells[(x, y)].custom_state(True)
                        self.update_living_cell(True)
                    else:
                        self.cells[(x, y)].custom_state(False)
                    x += settings.CELL
                x = position[0]
                y += settings.CELL
