from pathlib import PurePath

GAME_NAME = "GAME OF LIFE"

# Frame per second.
FPS = 30

# Paths to files in the project
BASE_DIR = PurePath(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
IMAGE_DIR = DATA_DIR / "images"
FONT_DIR = DATA_DIR / "fonts"
TEXT_DIR = DATA_DIR / "text"

# File paths to important files.
# NOTE: Need to convert the paths to strings because pygame can't handle pathlib paths yet.
ICON_FILE = str(IMAGE_DIR / "logo.png")
HEADER_FONT = str(FONT_DIR / "LLPIXEL3.ttf")
TEXT_FONT = str(FONT_DIR / "Rheiborn_Sans_Clean.ttf")
PATTERN_LIST = TEXT_DIR / "patterns.txt"

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
WINDOW_SIZE = (WIDTH, HEIGHT)

# Settings for the viewport size and position on the screen.
BOARD_X_POS = 250
BOARD_Y_POS = 30
BOARD_WIDTH_SIZE = 980
BOARD_HEIGHT_SIZE = 620

# Media control buttons.
CONTROLS_BUTTON_SIZE = 30
CONTROLS_GAP = 12
CONTROLS_Y = BOARD_Y_POS + BOARD_HEIGHT_SIZE + 15
CONTROLS_COLOR = (120, 120, 120)
CONTROLS_ACTIVE_COLOR = (255, 255, 255)
CONTROLS_HOVER_COLOR = (200, 200, 200)

# Camera / zoom settings.
DEFAULT_ZOOM = 10.0
MIN_ZOOM = 0.5
MAX_ZOOM = 100.0
ZOOM_FACTOR = 1.15

# Mouse buttons.
LEFT_CLICK = (True, False, False)
MIDDLE_CLICK = 2
RIGHT_CLICK = (False, False, True)
SCROLL_DOWN = 5
SCROLL_UP = 4

# Text sizes.
H1 = 100
H2 = 35
H3 = 25
H4 = 20
TEXT = 15
