# GAME OF LIFE

Game of life is an algorithm invented by John Horton Conway in 1970. The game of life is set on a 2-dimensional grid made up by many small cells. Each cells is in one of two states, alive or dead. A cells state is decided by the algorithm, which has four simple rules.

## RULES

1. A cell dies if it has less than two living neighbors.
2. A cell survives until the next generation if it has two or three neighbors.
3. A cell with more than three neighbors dies.
4. A dead cell with exactly three neighbors turns into a living cell.

## DEMO

![Demonstration of game of life](/assets/demo.gif)

## CONTROLS

- Start with `Enter`
- Pause with `P`
- Reset grid with `R`
- Quit program with `Esc`
- Toogle fullscreen with `F11`
- Click or hold the `Left mouse button` to draw cells.
- Click or hold the `Right mouse button` to erase cells.
- Press `Up` or `Down` or use the `mouse wheel` to choose a predefined pattern.
- Hold down `Left Ctrl` + `Left mouse button` to place out predefined patterns.

## BUILT WITH

- [Python 3.6.7](https://www.python.org/)
- [Pygame 1.9.6](https://www.pygame.org/)
