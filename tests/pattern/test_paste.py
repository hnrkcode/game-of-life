import pytest

from gameoflife.pattern.paste import PastePattern, get_pattern_matrix


def test_get_pattern_matrix_returns_pattern_for_valid_name() -> None:
    patterns = {"glider": [[1, 0], [0, 1]]}
    assert get_pattern_matrix(patterns, "glider") == [[1, 0], [0, 1]]


def test_get_pattern_matrix_returns_default_for_none() -> None:
    patterns = {"glider": [[1, 0], [0, 1]]}
    assert get_pattern_matrix(patterns, None) == [[1]]


def test_get_pattern_matrix_returns_default_for_empty_string() -> None:
    patterns = {"glider": [[1, 0], [0, 1]]}
    assert get_pattern_matrix(patterns, "") == [[1]]


# ---------------------------------------------------------------------------
# PastePattern transform integration
# ---------------------------------------------------------------------------


@pytest.fixture()
def paste() -> PastePattern:
    return PastePattern()


class TestGetEffectiveMatrix:
    def test_returns_raw_when_no_transform(self, paste: PastePattern) -> None:
        name = next(iter(paste.pattern))
        assert paste.get_effective_matrix(name) == paste.pattern[name]

    def test_returns_transformed_after_rotation(self, paste: PastePattern) -> None:
        name = next(iter(paste.pattern))
        paste.rotate_pattern_cw(name)
        # Should differ for non-square or asymmetric patterns — just check it's set.
        assert paste._transformed is not None
        assert paste.get_effective_matrix(name) is paste._transformed

    def test_returns_raw_after_reset(self, paste: PastePattern) -> None:
        name = next(iter(paste.pattern))
        paste.rotate_pattern_cw(name)
        paste.reset_transform()
        assert paste._transformed is None
        assert paste.get_effective_matrix(name) == paste.pattern[name]


class TestTransformRoundTrips:
    def test_four_cw_rotations_return_to_original(self, paste: PastePattern) -> None:
        name = next(iter(paste.pattern))
        original = paste.pattern[name]
        for _ in range(4):
            paste.rotate_pattern_cw(name)
        assert paste.get_effective_matrix(name) == original

    def test_four_ccw_rotations_return_to_original(self, paste: PastePattern) -> None:
        name = next(iter(paste.pattern))
        original = paste.pattern[name]
        for _ in range(4):
            paste.rotate_pattern_ccw(name)
        assert paste.get_effective_matrix(name) == original

    def test_double_flip_h_returns_to_original(self, paste: PastePattern) -> None:
        name = next(iter(paste.pattern))
        original = paste.pattern[name]
        paste.flip_pattern_h(name)
        paste.flip_pattern_h(name)
        assert paste.get_effective_matrix(name) == original

    def test_double_flip_v_returns_to_original(self, paste: PastePattern) -> None:
        name = next(iter(paste.pattern))
        original = paste.pattern[name]
        paste.flip_pattern_v(name)
        paste.flip_pattern_v(name)
        assert paste.get_effective_matrix(name) == original
