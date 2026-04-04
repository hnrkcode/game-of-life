import pygame
import pytest

from gameoflife import settings
from gameoflife.app import handle_control_action, has_finished, is_inside_viewport, is_pausable, preview_patterns
from gameoflife.board.cell import Cell
from gameoflife.camera import Camera
from gameoflife.pattern.paste import PastePattern


def make_camera(**kwargs: float) -> Camera:
    defaults: dict[str, float] = {
        "viewport_x": 0,
        "viewport_y": 0,
        "viewport_w": 200,
        "viewport_h": 200,
        "cell_size": 10.0,
    }
    defaults.update(kwargs)
    return Camera(**defaults)  # type: ignore[arg-type]


def test_is_inside_viewport_fully_inside() -> None:
    camera = make_camera()
    pattern = pygame.Surface((10, 10))
    assert is_inside_viewport((50, 50), pattern, camera) is True


def test_is_inside_viewport_at_origin() -> None:
    camera = make_camera()
    pattern = pygame.Surface((10, 10))
    assert is_inside_viewport((0, 0), pattern, camera) is True


def test_is_inside_viewport_at_bottom_right_edge() -> None:
    camera = make_camera()
    pattern = pygame.Surface((10, 10))
    assert is_inside_viewport((190, 190), pattern, camera) is True


def test_is_inside_viewport_overflows_right() -> None:
    camera = make_camera()
    pattern = pygame.Surface((20, 10))
    assert is_inside_viewport((185, 50), pattern, camera) is False


def test_is_inside_viewport_overflows_bottom() -> None:
    camera = make_camera()
    pattern = pygame.Surface((10, 20))
    assert is_inside_viewport((50, 185), pattern, camera) is False


def test_is_inside_viewport_before_left_edge() -> None:
    camera = make_camera(viewport_x=100)
    pattern = pygame.Surface((10, 10))
    assert is_inside_viewport((50, 50), pattern, camera) is False


def test_is_inside_viewport_before_top_edge() -> None:
    camera = make_camera(viewport_y=100)
    pattern = pygame.Surface((10, 10))
    assert is_inside_viewport((50, 50), pattern, camera) is False


def test_preview_patterns_uses_green_when_inside_viewport(monkeypatch: pytest.MonkeyPatch) -> None:
    camera = make_camera()
    grid = PastePattern()
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (50, 50))

    surface, _ = preview_patterns(is_ctrl_held=False, grid=grid, pattern_name=None, camera=camera)

    # The default single-cell preview is 10x10; at (50,50) it fits within 200x200 viewport.
    pixel_color = surface.get_at((0, 0))[:3]
    assert pixel_color == settings.PASTE_ON


def test_preview_patterns_uses_red_when_outside_viewport(monkeypatch: pytest.MonkeyPatch) -> None:
    camera = make_camera()
    grid = PastePattern()
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (500, 500))

    surface, _ = preview_patterns(is_ctrl_held=False, grid=grid, pattern_name=None, camera=camera)

    pixel_color = surface.get_at((0, 0))[:3]
    assert pixel_color == settings.PASTE_OFF


def test_preview_patterns_uses_red_when_pattern_overflows_viewport(monkeypatch: pytest.MonkeyPatch) -> None:
    camera = make_camera()
    grid = PastePattern()
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (195, 195))

    # Default single-cell preview is 10x10, so at (195,195) it overflows a 200x200 viewport.
    surface, _ = preview_patterns(is_ctrl_held=False, grid=grid, pattern_name=None, camera=camera)

    pixel_color = surface.get_at((0, 0))[:3]
    assert pixel_color == settings.PASTE_OFF


def test_preview_patterns_returns_mouse_position(monkeypatch: pytest.MonkeyPatch) -> None:
    camera = make_camera()
    grid = PastePattern()
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (42, 99))

    _, pos = preview_patterns(is_ctrl_held=False, grid=grid, pattern_name=None, camera=camera)

    assert pos == (42, 99)


def test_paste_only_allowed_inside_viewport() -> None:
    camera = make_camera()
    grid = PastePattern()

    # Position inside the viewport, paste should add cells.
    world_pos = camera.screen_to_world(50, 50)
    assert camera.is_in_viewport(50, 50) is True
    grid.paste(world_pos=world_pos, button=settings.LEFT_CLICK)
    assert len(grid.cell_sprite) == 1

    grid.reset()

    # Position outside the viewport, paste must be guarded by is_in_viewport.
    assert camera.is_in_viewport(500, 500) is False


def test_has_finished_returns_true_when_no_cells_alive_and_generation_greater_than_zero() -> None:
    grid = PastePattern()
    grid.generation = 1
    assert has_finished(grid) is True


def test_has_finished_returns_false_when_cells_alive() -> None:
    grid = PastePattern()
    grid.cell_sprite[(0, 0)] = Cell()
    grid.generation = 1
    assert has_finished(grid) is False


def test_has_finished_returns_false_when_generation_zero() -> None:
    grid = PastePattern()
    assert has_finished(grid) is False


def test_has_finished_returns_false_when_cells_alive_and_generation_zero() -> None:
    grid = PastePattern()
    grid.cell_sprite[(0, 0)] = Cell()
    assert has_finished(grid) is False


def test_is_pausable_returns_true_when_cells_alive_and_generation_greater_than_zero() -> None:
    grid = PastePattern()
    grid.cell_sprite[(0, 0)] = Cell()
    grid.generation = 1
    assert is_pausable(grid) is True


def test_is_pausable_returns_false_when_no_cells_alive() -> None:
    grid = PastePattern()
    grid.generation = 1
    assert is_pausable(grid) is False


def test_is_pausable_returns_false_when_generation_zero() -> None:
    grid = PastePattern()
    assert is_pausable(grid) is False


def _make_finished_grid() -> PastePattern:
    """Return a grid with one step of history and no living cells (finished state)."""
    grid = PastePattern()
    grid.cell_sprite[(0, 0)] = Cell()
    grid.cell[(0, 0)] = 1
    grid.update()  # advances generation; the alive cell dies (no neighbours → death)
    return grid


def test_handle_control_action_stop_resets_grid_and_clears_finished() -> None:
    grid = _make_finished_grid()
    is_paused, is_finished = handle_control_action("stop", grid, False, True)
    assert is_finished is False
    assert is_paused is False
    assert grid.generation == 0


def test_handle_control_action_skip_back_clears_finished() -> None:
    grid = _make_finished_grid()
    _, is_finished = handle_control_action("skip_back", grid, False, True)
    assert is_finished is False


def test_handle_control_action_skip_forward_clears_finished() -> None:
    grid = _make_finished_grid()
    _, is_finished = handle_control_action("skip_forward", grid, False, True)
    assert is_finished is False


def test_handle_control_action_rewind_clears_finished() -> None:
    grid = _make_finished_grid()
    _, is_finished = handle_control_action("rewind", grid, False, True)
    assert is_finished is False
    assert grid.direction == "backward"


def test_handle_control_action_fast_forward_clears_finished() -> None:
    grid = _make_finished_grid()
    _, is_finished = handle_control_action("fast_forward", grid, False, True)
    assert is_finished is False
    assert grid.direction == "forward"


def test_handle_control_action_play_pause_starts_and_clears_finished() -> None:
    grid = _make_finished_grid()
    # grid has history so play should be allowed
    is_paused, is_finished = handle_control_action("play_pause", grid, True, True)
    assert is_paused is False
    assert is_finished is False
    assert grid.run is True


def test_handle_control_action_play_pause_pauses_does_not_change_finished() -> None:
    grid = PastePattern()
    grid.cell_sprite[(0, 0)] = Cell()
    grid.cell[(0, 0)] = 1
    grid.generation = 1
    grid.start()
    is_paused, is_finished = handle_control_action("play_pause", grid, False, False)
    assert is_paused is True
    assert is_finished is False  # was already False, must remain False
    assert grid.run is False


def test_handle_control_action_play_pause_no_cells_no_history_does_not_start() -> None:
    grid = PastePattern()
    is_paused, _ = handle_control_action("play_pause", grid, False, False)
    assert is_paused is False
    assert grid.run is False
