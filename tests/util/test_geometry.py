from gameoflife.util.geometry import bresenham_line


def test_single_point():
    assert bresenham_line(0, 0, 0, 0) == [(0, 0)]


def test_horizontal_line():
    assert bresenham_line(0, 0, 3, 0) == [(0, 0), (1, 0), (2, 0), (3, 0)]


def test_vertical_line():
    assert bresenham_line(0, 0, 0, 3) == [(0, 0), (0, 1), (0, 2), (0, 3)]


def test_diagonal_line():
    assert bresenham_line(0, 0, 3, 3) == [(0, 0), (1, 1), (2, 2), (3, 3)]


def test_negative_direction():
    points = bresenham_line(3, 3, 0, 0)
    assert points[0] == (3, 3)
    assert points[-1] == (0, 0)
    assert len(points) == 4


def test_steep_line():
    points = bresenham_line(0, 0, 1, 4)
    assert points[0] == (0, 0)
    assert points[-1] == (1, 4)
    assert len(points) == 5


def test_shallow_line():
    points = bresenham_line(0, 0, 4, 1)
    assert points[0] == (0, 0)
    assert points[-1] == (4, 1)
    assert len(points) == 5
