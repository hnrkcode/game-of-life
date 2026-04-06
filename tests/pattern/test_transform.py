from gameoflife.pattern.transform import (
    flip_horizontal,
    flip_vertical,
    rotate_ccw,
    rotate_cw,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SQUARE = [
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
]

RECT = [
    [1, 0, 0],
    [1, 1, 1],
]

BLINKER = [[1, 1, 1]]

SINGLE = [[1]]


# ---------------------------------------------------------------------------
# rotate_cw
# ---------------------------------------------------------------------------


class TestRotateCW:
    def test_square(self) -> None:
        assert rotate_cw(SQUARE) == [
            [0, 0, 1],
            [0, 1, 1],
            [1, 0, 0],
        ]

    def test_rect(self) -> None:
        assert rotate_cw(RECT) == [
            [1, 1],
            [1, 0],
            [1, 0],
        ]

    def test_blinker(self) -> None:
        assert rotate_cw(BLINKER) == [[1], [1], [1]]

    def test_single(self) -> None:
        assert rotate_cw(SINGLE) == [[1]]

    def test_four_rotations_return_to_original(self) -> None:
        m = RECT
        for _ in range(4):
            m = rotate_cw(m)
        assert m == RECT


# ---------------------------------------------------------------------------
# rotate_ccw
# ---------------------------------------------------------------------------


class TestRotateCCW:
    def test_square(self) -> None:
        assert rotate_ccw(SQUARE) == [
            [0, 0, 1],
            [1, 1, 0],
            [1, 0, 0],
        ]

    def test_rect(self) -> None:
        assert rotate_ccw(RECT) == [
            [0, 1],
            [0, 1],
            [1, 1],
        ]

    def test_four_rotations_return_to_original(self) -> None:
        m = RECT
        for _ in range(4):
            m = rotate_ccw(m)
        assert m == RECT

    def test_cw_then_ccw_is_identity(self) -> None:
        assert rotate_ccw(rotate_cw(SQUARE)) == SQUARE

    def test_ccw_then_cw_is_identity(self) -> None:
        assert rotate_cw(rotate_ccw(RECT)) == RECT


# ---------------------------------------------------------------------------
# flip_horizontal
# ---------------------------------------------------------------------------


class TestFlipHorizontal:
    def test_square(self) -> None:
        assert flip_horizontal(SQUARE) == [
            [0, 1, 1],
            [0, 1, 0],
            [1, 0, 0],
        ]

    def test_rect(self) -> None:
        assert flip_horizontal(RECT) == [
            [0, 0, 1],
            [1, 1, 1],
        ]

    def test_double_flip_is_identity(self) -> None:
        assert flip_horizontal(flip_horizontal(RECT)) == RECT

    def test_symmetric_pattern_unchanged(self) -> None:
        sym = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        assert flip_horizontal(sym) == sym


# ---------------------------------------------------------------------------
# flip_vertical
# ---------------------------------------------------------------------------


class TestFlipVertical:
    def test_square(self) -> None:
        assert flip_vertical(SQUARE) == [
            [0, 0, 1],
            [0, 1, 0],
            [1, 1, 0],
        ]

    def test_rect(self) -> None:
        assert flip_vertical(RECT) == [
            [1, 1, 1],
            [1, 0, 0],
        ]

    def test_double_flip_is_identity(self) -> None:
        assert flip_vertical(flip_vertical(RECT)) == RECT


# ---------------------------------------------------------------------------
# Compositions
# ---------------------------------------------------------------------------


class TestCompositions:
    def test_rotate_cw_twice_equals_flip_both(self) -> None:
        """180° rotation == flip horizontal then vertical (or vice versa)."""
        rotated = rotate_cw(rotate_cw(SQUARE))
        flipped = flip_vertical(flip_horizontal(SQUARE))
        assert rotated == flipped

    def test_does_not_mutate_input(self) -> None:
        original = [[1, 0], [0, 1]]
        copy = [row[:] for row in original]
        rotate_cw(original)
        rotate_ccw(original)
        flip_horizontal(original)
        flip_vertical(original)
        assert original == copy
