# Game of life

> Python implementation of Conway's game of life algorithm

[![made-with-pygame](https://img.shields.io/badge/Made%20with-Pygame-green.svg)](https://www.pygame.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Generic badge](https://img.shields.io/badge/code_style-black-black.svg)](https://github.com/psf/black)

![Demonstration of game of life](/data/demo.gif)

Game of life is an algorithm invented by John Horton Conway in 1970. The game of life is set on a 2-dimensional grid made up by many small cells. Each cells is in one of two states, alive or dead. A cells state is decided by the algorithm, which has four simple rules:

>1. A cell dies if it has less than two living neighbors.
2. A cell survives until the next generation if it has two or three neighbors.
3. A cell with more than three neighbors dies.
4. A dead cell with exactly three neighbors turns into a living cell.

## Setup

#### Create & activate virtual environment

It's recommended to install the package and all it's dependencies in a virtual environment.

```sh
python -m venv gameoflife_venv
```
```sh
source gameoflife_venv/bin/activate
```

#### Install package & requirements

```sh
pip install -r requirements.txt .
```

#### Editable mode

Install package in editable mode to be able to develop and test the code without uninstall and reinstall over and over again.

```sh
pip install -r requirements.txt -e .
```

#### uninstall package & requirements

```sh
pip uninstall -r requirements.txt gameoflife
```

## Usage

| key | description |
|:-----|-------|
| `P`     | Pause algorithm |
| `R`     | Remove all cells from the board |
| `F11`   | Toggle on/off fullscreen |
| `ESC`   | Quit program |
| `Enter` | Run algorithm |
| `LEFT MOUSE BUTTON` | Click or hold to draw new cells |
| `RIGHT MOUSE BUTTON` | Click or hold to erase cells |
| `UP` `DOWN` `SCROLL WHEEL` | Choose pattern from predefined patterns |
| `LEFT CTRL` + `LEFT MOUSE BUTTON` | Paste chosen pattern onto the grid |
