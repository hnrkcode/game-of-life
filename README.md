# Game of life

[![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![made-with-pygame](https://img.shields.io/badge/Made%20with-Pygame-c1fb25.svg?logo=pygame)](https://github.com/pygame/pygame)
[![Package manager: uv](https://img.shields.io/badge/package%20manager-uv-de5fea?logo=astral&logoColor=de5fea)](https://github.com/astral-sh/uv)
[![code style: ruff](https://img.shields.io/badge/code%20style-ruff-d7ff64?logo=ruff&logoColor=d7ff64)](https://github.com/astral-sh/ruff)
[![type checked: ty](https://custom-icon-badges.demolab.com/badge/type%20checked-ty-47eae2.svg?logo=ty-astral-logo&labelColor=gray&color=47eae2&logoColor=47eae2)](https://github.com/astral-sh/ty)
[![codecov](https://codecov.io/github/hnrkcode/game-of-life/graph/badge.svg?token=H0AFNO51XV)](https://codecov.io/github/hnrkcode/game-of-life)
[![License: MIT](https://img.shields.io/badge/License-MIT-40a43b.svg?logo=opensourceinitiative&logoColor=40a43b)](https://opensource.org/licenses/MIT)

Python implementation of Conway's game of life algorithm

![Demonstration of game of life](/data/demo.gif)

Game of life is an algorithm invented by John Horton Conway in 1970. The game of life is set on a 2-dimensional grid made up by many small cells. Each cells is in one of two states, alive or dead. A cells state is decided by the algorithm, which has four simple rules:

1. A cell dies if it has less than two living neighbors.
2. A cell survives until the next generation if it has two or three neighbors.
3. A cell with more than three neighbors dies.
4. A dead cell with exactly three neighbors turns into a living cell.

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for fast Python dependency management. All dependencies are defined in `pyproject.toml`.

1. Create and activate a virtual environment (if not already active):

    ```bash
    uv venv
    source .venv/bin/activate
    ```

    (The `.venv` folder is created by default.)

3. Install all dependencies (including dev dependencies):

    ```bash
    uv sync --all-groups
    ```

4. Run the game:

    ```bash
    make start
    ```

## Controls

| key | description |
|:-----|-------|
| `P`     | Pause algorithm |
| `R`     | Remove all cells from the board |
| `F11`   | Toggle on/off fullscreen |
| `ESC`   | Quit program |
| `Enter` | Run algorithm |
| `LEFT MOUSE BUTTON` | Click or hold to draw new cells |
| `RIGHT MOUSE BUTTON` | Click or hold to erase cells |
| `UP`, `DOWN` or `SCROLL WHEEL` | Choose pattern from predefined patterns |
| Hold `CTRL` + click `LEFT MOUSE BUTTON` | Paste chosen pattern onto the grid |

## Commands

The following commands are available for development tasks:

| Command         | Description                      |
|-----------------|----------------------------------|
| `make start`    | Run the game                     |
| `make test`     | Run all pytests with coverage    |
| `make lint`     | Lint code with Ruff              |
| `make format`   | Format code with Ruff            |
| `make typecheck`| Type check code with Ty          |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.