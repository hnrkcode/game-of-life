#!/usr/bin/env python3.6

import os.path

# Frame per second.
FPS = 30

# File paths to important files.
ICON_FILE = os.path.join('assets', 'img', 'logo.png')
HEADER = os.path.join('assets', 'font', 'LLPIXEL3.ttf')
FONT = os.path.join('assets', 'font', 'Rheiborn_Sans_Clean.ttf')

# Color settings.
TEXT_COLOR = (150, 150, 150)
BG_COLOR = (19, 19, 19)
DEAD = (27, 27, 27)
ALIVE = (150, 150, 150)
GEN1 = (40, 160, 255)
GEN2 = (0, 255, 206)
GEN3 = (233, 255, 131)
GEN4 = (255, 141, 61)
GEN5 = (232, 0, 25)

# Window size.
WIDTH = 1280
HEIGHT = 720

# Cell size.
CELL = 10

# Settings for the 2D grids size and position on the screen.
BOARD_X_POS = 250
BOARD_Y_POS = 50
BOARD_WIDTH_SIZE = 980
BOARD_HEIGHT_SIZE = 620
BOARD_WIDTH = int(BOARD_WIDTH_SIZE / CELL)
BOARD_HEIGHT = int(BOARD_HEIGHT_SIZE / CELL)

# Grids border limits.
MIN_X = BOARD_X_POS
MAX_X = BOARD_X_POS + BOARD_WIDTH_SIZE - CELL
MIN_Y = BOARD_Y_POS
MAX_Y = BOARD_Y_POS + BOARD_HEIGHT_SIZE - CELL

# Maximum amount of cells that can exist on the grid.
TOTAL_CELLS = BOARD_WIDTH * BOARD_HEIGHT

# Mouse buttons.
LEFT_CLICK = (1, 0, 0)
RIGHT_CLICK = (0, 0, 1)
SCROLL_DOWN = 5
SCROLL_UP = 4
