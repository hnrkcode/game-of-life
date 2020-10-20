import os.path

# Frame per second.
FPS = 30

# Paths to files in the project
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGE_DIR = os.path.join(DATA_DIR, "images")
FONT_DIR = os.path.join(DATA_DIR, "fonts")
TEXT_DIR = os.path.join(DATA_DIR, "text")

# File paths to important files.
ICON_FILE = os.path.join(IMAGE_DIR, "logo.png")
HEADER_FONT = os.path.join(FONT_DIR, "LLPIXEL3.ttf")
TEXT_FONT = os.path.join(FONT_DIR, "Rheiborn_Sans_Clean.ttf")
PATTERN_LIST = os.path.join(TEXT_DIR, "patterns.txt")

# Color settings.
TEXT_COLOR = (150, 150, 150)
BG_COLOR = (19, 19, 19)
MODAL_COLOR = (40, 40, 40)
OVERLAY_COLOR = (10, 10, 10)
DEAD = (27, 27, 27)
ALIVE = (150, 150, 150)
GEN1 = (40, 160, 255)
GEN2 = (0, 255, 206)
GEN3 = (233, 255, 131)
GEN4 = (255, 141, 61)
GEN5 = (232, 0, 25)

PASTE_ON = (138, 226, 52)
PASTE_OFF = (239, 41, 41)

# Pattern scroll list colors.
ACTIVE = (255, 255, 255)

# Window size.
WIDTH = 1280
HEIGHT = 720

# Cell size.
CELL_SIZE = 10

# Settings for the 2D grids size and position on the screen.
BOARD_X_POS = 250
BOARD_Y_POS = 50
BOARD_WIDTH_SIZE = 980
BOARD_HEIGHT_SIZE = 620
BOARD_WIDTH = int(BOARD_WIDTH_SIZE / CELL_SIZE)
BOARD_HEIGHT = int(BOARD_HEIGHT_SIZE / CELL_SIZE)

# Grids border limits.
MIN_X = BOARD_X_POS
MAX_X = BOARD_X_POS + BOARD_WIDTH_SIZE - CELL_SIZE
MIN_Y = BOARD_Y_POS
MAX_Y = BOARD_Y_POS + BOARD_HEIGHT_SIZE - CELL_SIZE

# Maximum amount of cells that can exist on the grid.
TOTAL_CELLS = BOARD_WIDTH * BOARD_HEIGHT

# Mouse buttons.
LEFT_CLICK = (1, 0, 0)
RIGHT_CLICK = (0, 0, 1)
SCROLL_DOWN = 5
SCROLL_UP = 4
