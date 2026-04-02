from gameoflife.camera import Camera


def make_camera(**kwargs: float) -> Camera:
    defaults: dict[str, float] = {
        "viewport_x": 250,
        "viewport_y": 50,
        "viewport_w": 980,
        "viewport_h": 620,
        "cell_size": 10.0,
    }
    defaults.update(kwargs)
    return Camera(**defaults)  # type: ignore[arg-type]


def test_world_to_screen_at_origin() -> None:
    cam = make_camera()
    # Cell (0,0) should map to the center of the viewport.
    sx, sy = cam.world_to_screen(0, 0)
    assert sx == 250 + 980 / 2
    assert sy == 50 + 620 / 2


def test_screen_to_world_at_center() -> None:
    cam = make_camera()
    # Center of viewport should map to world (0, 0).
    wx, wy = cam.screen_to_world(250 + 490, 50 + 310)
    assert wx == 0
    assert wy == 0


def test_screen_to_world_roundtrip() -> None:
    cam = make_camera()
    for wx, wy in [(0, 0), (10, -5), (-20, 30)]:
        sx, sy = cam.world_to_screen(wx, wy)
        rwx, rwy = cam.screen_to_world(int(sx), int(sy))
        assert rwx == wx
        assert rwy == wy


def test_get_visible_bounds() -> None:
    cam = make_camera()
    min_wx, min_wy, max_wx, max_wy = cam.get_visible_bounds()
    # With 980px viewport and 10px/cell, roughly 98 cells wide.
    assert max_wx - min_wx >= 97
    assert max_wy - min_wy >= 61


def test_zoom_changes_cell_size() -> None:
    cam = make_camera()
    original = cam.cell_size
    cam.zoom(2.0, 250 + 490, 50 + 310)
    assert cam.cell_size == original * 2.0


def test_zoom_clamped_min() -> None:
    cam = make_camera(min_cell_size=2.0)
    cam.zoom(0.01, 250 + 490, 50 + 310)
    assert cam.cell_size == 2.0


def test_zoom_clamped_max() -> None:
    cam = make_camera(max_cell_size=50.0)
    cam.zoom(100.0, 250 + 490, 50 + 310)
    assert cam.cell_size == 50.0


def test_pan_moves_center() -> None:
    cam = make_camera()
    original_x = cam.world_center_x
    original_y = cam.world_center_y
    cam.pan(100, 50)
    # Panning right on screen moves world center left.
    assert cam.world_center_x < original_x
    assert cam.world_center_y < original_y


def test_is_in_viewport() -> None:
    cam = make_camera()
    # Inside viewport.
    assert cam.is_in_viewport(500, 300) is True
    # In sidebar area (left of viewport).
    assert cam.is_in_viewport(100, 300) is False
    # Above viewport.
    assert cam.is_in_viewport(500, 10) is False
    # Right edge (exclusive).
    assert cam.is_in_viewport(250 + 980, 300) is False
    # Bottom edge (exclusive).
    assert cam.is_in_viewport(500, 50 + 620) is False
