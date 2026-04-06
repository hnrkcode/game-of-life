def rotate_cw(matrix: list[list[int]]) -> list[list[int]]:
    """Rotate a 2D matrix 90 degrees clockwise."""
    rows = len(matrix)
    cols = len(matrix[0])
    return [[matrix[rows - 1 - r][c] for r in range(rows)] for c in range(cols)]


def rotate_ccw(matrix: list[list[int]]) -> list[list[int]]:
    """Rotate a 2D matrix 90 degrees counter-clockwise."""
    rows = len(matrix)
    cols = len(matrix[0])
    return [[matrix[r][cols - 1 - c] for r in range(rows)] for c in range(cols)]


def flip_horizontal(matrix: list[list[int]]) -> list[list[int]]:
    """Mirror a 2D matrix left-to-right."""
    return [row[::-1] for row in matrix]


def flip_vertical(matrix: list[list[int]]) -> list[list[int]]:
    """Mirror a 2D matrix top-to-bottom."""
    return [row[:] for row in reversed(matrix)]
