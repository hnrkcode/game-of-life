from gameoflife.pattern.paste import get_pattern_matrix


def test_get_pattern_matrix_returns_pattern_for_valid_name() -> None:
    patterns = {"glider": [[1, 0], [0, 1]]}
    assert get_pattern_matrix(patterns, "glider") == [[1, 0], [0, 1]]


def test_get_pattern_matrix_returns_default_for_none() -> None:
    patterns = {"glider": [[1, 0], [0, 1]]}
    assert get_pattern_matrix(patterns, None) == [[1]]


def test_get_pattern_matrix_returns_default_for_empty_string() -> None:
    patterns = {"glider": [[1, 0], [0, 1]]}
    assert get_pattern_matrix(patterns, "") == [[1]]
