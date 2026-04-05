import asyncio
import math
import os
import sys

import pygame
from pygame.locals import (
    FULLSCREEN,
    K_DOWN,
    K_ESCAPE,
    K_F11,
    K_LCTRL,
    K_MINUS,
    K_PLUS,
    K_RCTRL,
    K_RETURN,
    K_UP,
    KEYDOWN,
    KEYUP,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
    QUIT,
    K_h,
    K_p,
    K_r,
)

from gameoflife import settings
from gameoflife.board import Board
from gameoflife.camera import Camera
from gameoflife.controls import MediaControls
from gameoflife.modal import Modal, Overlay, ScreenText
from gameoflife.pattern.menu import ScrollMenu
from gameoflife.pattern.paste import PastePattern
from gameoflife.util.geometry import bresenham_line
from gameoflife.util.text import InfoText

RUNNING_IN_PYGBAG = sys.platform == "emscripten"


async def run() -> None:
    # Center the window on the screen.
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    # Initialize pygame.
    pygame.font.init()
    pygame.display.init()
    pygame.display.set_caption(settings.GAME_NAME)
    pygame.display.set_icon(pygame.image.load(settings.ICON_FILE))
    screen = pygame.display.set_mode(settings.WINDOW_SIZE)
    clock = pygame.time.Clock()

    # Initialize state variables.
    is_paused = False
    is_finished = False
    is_ctrl_held = False
    is_mouse_held = False
    is_fullscreen = False
    is_modal_active = False
    is_splash_screen = True
    is_panning = False
    last_draw_world_pos: tuple[int, int] | None = None

    # Initialize camera.
    camera = Camera(
        viewport_x=settings.BOARD_X_POS,
        viewport_y=settings.BOARD_Y_POS,
        viewport_w=settings.BOARD_WIDTH_SIZE,
        viewport_h=settings.BOARD_HEIGHT_SIZE,
        cell_size=settings.DEFAULT_ZOOM,
        min_cell_size=settings.MIN_ZOOM,
        max_cell_size=settings.MAX_ZOOM,
    )

    # Initialize menu and board variables.
    grid: PastePattern = PastePattern()
    pattern_name, paste_pattern = grid.select.get_current()
    scroll_menu = ScrollMenu()
    menu_obj = scroll_menu.setup(grid.select)

    # Initialize splash screen.
    splash_start_num = 0
    splash_header = InfoText(
        settings.GAME_NAME,
        size=settings.H1,
        font=settings.HEADER_FONT,
    )

    splash_header.set_position(
        (
            int(settings.WIDTH / 2 - (splash_header.image.get_width() / 2)),
            int(settings.HEIGHT / 3),
        )
    )

    splash_start = InfoText(
        "Press to start",
        size=settings.H2,
    )

    splash_start.set_position(
        (
            int(settings.WIDTH / 2 - (splash_start.image.get_width() / 2)),
            int(settings.HEIGHT / 1.75),
        )
    )

    splash_screen_group = pygame.sprite.RenderUpdates(splash_header, splash_start)

    # Version label in the bottom left corner.
    version_label = InfoText(f"v{settings.VERSION}", size=settings.TEXT)
    version_label.set_position((10, settings.HEIGHT - version_label.image.get_height() - 10))

    # Layout the text on the left side of the board.
    sidebar_layout = [
        InfoText("INFORMATION", size=settings.H3),
        InfoText(f"Generation: {grid.generation}", size=settings.TEXT),
        InfoText(f"Cells: {get_cell_count(grid)}", size=settings.TEXT),
        InfoText(f"Total deaths: {grid.deaths}", size=settings.TEXT),
        InfoText(f"Zoom: {camera.cell_size:.1f}x", size=settings.TEXT),
        InfoText(f"FPS: {clock.get_fps():.1f}", size=settings.TEXT),
        InfoText(None, size=settings.TEXT),
        *scroll_menu.format("PATTERNS", pattern_name, menu_obj),
        InfoText(None, size=settings.TEXT),
        InfoText("HELP", size=settings.H3),
        InfoText("Press (H) for help", size=settings.TEXT),
    ]

    sidebar_text = format_sidebar(sidebar_layout)
    sidebar_group = pygame.sprite.RenderUpdates(sidebar_text)

    # Background color of the board.
    board = Board()
    board_bg_group = pygame.sprite.RenderUpdates(board)

    # Modal that can be toggled to show help information.
    modal_box = Modal()
    modal_overlay = Overlay()
    modal_group = pygame.sprite.RenderUpdates(modal_overlay, modal_box)

    # Is shown when the user has paused the game.
    pause_screen = ScreenText("PAUSE")
    pause_screen_group = pygame.sprite.RenderUpdates(pause_screen)

    # Is shown when all cells have died.
    end_screen = ScreenText("GAMEOVER")
    end_screen_group = pygame.sprite.RenderUpdates(end_screen)

    # Media control buttons.
    controls = MediaControls()

    # Update pause text intervall.
    pygame.time.set_timer(pygame.USEREVENT, 200)

    while True:
        # Control the frame rate.
        clock.tick(settings.FPS)
        screen.fill(settings.BG_COLOR)

        # Handel user inputs.
        for event in pygame.event.get():
            # Exit the program.
            if (event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)) and not RUNNING_IN_PYGBAG:
                return

            # Press F11 to toggle to fullscreen mode.
            if event.type == KEYDOWN and event.key == K_F11 and not RUNNING_IN_PYGBAG:
                is_fullscreen, screen = toggle_fullscreen(is_fullscreen)

            # Events captured only while splash screen is running.
            if is_splash_screen:
                if event.type == pygame.USEREVENT:
                    splash_start.rect[1] = int(settings.HEIGHT / 1.75 + 5 * math.sin(splash_start_num) + 5)
                    splash_start_num += 1

                # Press any keyboard key or mouse button to close splash screen and start game.
                elif event.type in {KEYDOWN, MOUSEBUTTONDOWN}:
                    del splash_screen_group
                    del splash_header
                    del splash_start
                    del splash_start_num
                    is_splash_screen = False

            # Events captured only after splash screen is closed.
            else:
                # Update pause text.
                if event.type == pygame.USEREVENT and is_paused:
                    pause_screen_group.update()

                # Update end text.
                elif event.type == pygame.USEREVENT and not get_cell_count(grid) and grid.generation:
                    end_screen_group.update()

                # Toggle modal.
                elif event.type == KEYDOWN and event.key == K_h:
                    is_modal_active = toggle_modal(grid, is_modal_active, is_paused)

                # User can only interact with the board when the modal isn't active.
                if not is_modal_active:
                    if event.type == KEYDOWN:
                        # Press Enter to start the simulation if there are any cells on the board.
                        if event.key == K_RETURN and get_cell_count(grid):
                            grid.start()
                            is_paused = False

                        # Press R to clear the screen.
                        if event.key == K_r:
                            grid.reset()
                            is_paused, is_finished = False, False

                        # Press P to stop the simulation temporarily.
                        # Can only pause if there are cells and the generation is more than zero.
                        if event.key == K_p and is_pausable(grid):
                            if is_paused:
                                grid.start()
                            else:
                                grid.stop()
                            is_paused = not is_paused

                        # Choose predefined pattern.
                        if event.key == K_UP:
                            grid.select.previous()
                            pattern_name, paste_pattern = grid.select.get_current()
                            menu_obj = scroll_menu.setup(grid.select)

                        if event.key == K_DOWN:
                            grid.select.next()
                            pattern_name, paste_pattern = grid.select.get_current()
                            menu_obj = scroll_menu.setup(grid.select)

                        # Hold left control button to paste pattern when left clicking.
                        if event.key in {K_LCTRL, K_RCTRL}:
                            is_ctrl_held = True

                        # Zoom in/out with +/- keys.
                        if event.key == K_PLUS:
                            camera.zoom(settings.ZOOM_FACTOR, *viewport_center(camera))
                        if event.key == K_MINUS:
                            camera.zoom(1.0 / settings.ZOOM_FACTOR, *viewport_center(camera))

                    elif event.type == KEYUP and event.key in {K_LCTRL, K_RCTRL}:
                        is_ctrl_held = False

                    elif event.type == MOUSEBUTTONDOWN:
                        mods = pygame.key.get_mods()

                        # Scroll to zoom.
                        if event.button == settings.SCROLL_UP and not (mods & pygame.KMOD_LCTRL):
                            camera.zoom(settings.ZOOM_FACTOR, *pygame.mouse.get_pos())
                        elif event.button == settings.SCROLL_DOWN and not (mods & pygame.KMOD_LCTRL):
                            camera.zoom(1.0 / settings.ZOOM_FACTOR, *pygame.mouse.get_pos())

                        # Scroll through patterns (with CTRL).
                        elif event.button == settings.SCROLL_DOWN and (mods & pygame.KMOD_LCTRL):
                            grid.select.next()
                            pattern_name, paste_pattern = grid.select.get_current()
                            menu_obj = scroll_menu.setup(grid.select)
                        elif event.button == settings.SCROLL_UP and (mods & pygame.KMOD_LCTRL):
                            grid.select.previous()
                            pattern_name, paste_pattern = grid.select.get_current()
                            menu_obj = scroll_menu.setup(grid.select)

                        # Middle mouse button to start panning.
                        elif event.button == settings.MIDDLE_CLICK:
                            is_panning = True

                        # Left click to deploy cells or right click to remove cells.
                        else:
                            # Check media control buttons first.
                            action = controls.handle_click(event.pos)
                            if action:
                                is_paused, is_finished = handle_control_action(
                                    action,
                                    grid,
                                    is_paused,
                                    is_finished,
                                )
                            else:
                                if is_finished:
                                    grid.reset()
                                    is_paused, is_finished = False, False
                                is_mouse_held = True

                    elif event.type == MOUSEBUTTONUP:
                        if event.button == settings.MIDDLE_CLICK:
                            is_panning = False
                        else:
                            is_mouse_held = False
                            last_draw_world_pos = None

                    # Pan with middle mouse drag.
                    elif event.type == MOUSEMOTION and is_panning:
                        camera.pan(event.rel[0], event.rel[1])

        if is_splash_screen:
            splash_screen_group.draw(screen)
        else:
            # Draw/erase cells on the grid.
            if is_mouse_held:
                pos = pygame.mouse.get_pos()
                button = pygame.mouse.get_pressed()

                if camera.is_in_viewport(*pos):
                    world_pos = camera.screen_to_world(*pos)

                    # Interpolate between last and current position to fill gaps
                    # caused by fast mouse movement.
                    if last_draw_world_pos is not None and last_draw_world_pos != world_pos:
                        points = bresenham_line(*last_draw_world_pos, *world_pos)
                    else:
                        points = [world_pos]

                    for pt in points:
                        if is_ctrl_held:
                            paste_pattern(world_pos=pt, button=button, name=pattern_name)
                        else:
                            paste_pattern(world_pos=pt, button=button)

                    last_draw_world_pos = world_pos

            # Update the grid.
            if grid.run:
                if grid.direction == "forward":
                    grid.update()
                elif not grid.step_back():
                    grid.stop()
                    is_paused = True

            # Update runtime information.
            sidebar_text[1].update(f"Generation: {grid.generation}")
            sidebar_text[2].update(f"Cells: {get_cell_count(grid)}")
            sidebar_text[3].update(f"Total deaths: {grid.deaths}")
            sidebar_text[4].update(f"Zoom: {camera.cell_size:.1f}x")
            sidebar_text[5].update(f"FPS: {clock.get_fps():.1f}")

            # Update pattern scroll menu.
            scroll_menu.update(
                display=sidebar_text,
                menu=menu_obj,
                active=pattern_name,
                start=8,
                end=19,
            )

            # Draw everything to the screen.
            sidebar_group.draw(screen)
            board_bg_group.draw(screen)

            # Preview of cell or selected pattern.
            preview = preview_patterns(is_ctrl_held, grid, pattern_name, camera)
            screen.blit(*preview)

            # Clip rendering to viewport so cells don't bleed into sidebar.
            screen.set_clip(pygame.Rect(camera.viewport_x, camera.viewport_y, camera.viewport_w, camera.viewport_h))

            # Render only visible cells.
            min_wx, min_wy, max_wx, max_wy = camera.get_visible_bounds()
            cell_px = max(1, int(camera.cell_size))
            for key, value in grid.cell.items():
                if value == 1:
                    wx, wy = key
                    if min_wx <= wx <= max_wx and min_wy <= wy <= max_wy:
                        sx, sy = camera.world_to_screen(wx, wy)
                        pygame.draw.rect(
                            screen,
                            grid.cell_sprite[key].color,
                            pygame.Rect(int(sx), int(sy), cell_px, cell_px),
                        )

            screen.set_clip(None)

            if is_paused:
                pause_screen_group.draw(screen)

            # Show end screen when there are no more cells left on the board.
            if has_finished(grid):
                grid.stop()
                end_screen_group.draw(screen)
                is_finished = True
                is_paused = False

            # Draw media controls.
            controls.draw(screen, grid.run, grid.direction)

            if is_modal_active:
                modal_group.draw(screen)

        screen.blit(version_label.image, version_label.rect)
        pygame.display.update()
        await asyncio.sleep(0)


def format_sidebar(lines: list[InfoText]) -> list[InfoText]:
    """Arrange the sidebars text lines on the screen."""
    x, y = 30, settings.BOARD_Y_POS

    for line in lines:
        line.set_position((x, y))
        # Add different vertical space depending on font size.
        y = (y + 40) if line.fontsize > settings.TEXT else (y + 20)

    return lines


def get_cell_count(grid: PastePattern) -> int:
    """Return number alive cells on the grid."""
    return len(grid.cell_sprite)


def has_finished(grid: PastePattern) -> bool:
    """Return true when atleast one generation has passed and all cells are dead."""
    return not get_cell_count(grid) and grid.generation > 0


def is_pausable(grid: PastePattern) -> bool:
    """Check if the game can be paused."""
    # Can only pause when there are alive cells and
    return get_cell_count(grid) > 0 and grid.generation > 0


def is_inside_viewport(pos: tuple[int, int], pattern: pygame.Surface, camera: Camera) -> bool:
    """Check if the pattern preview fits entirely within the viewport."""
    x, y = pos
    w, h = pattern.get_size()
    return (
        camera.viewport_x <= x
        and camera.viewport_y <= y
        and x + w <= camera.viewport_x + camera.viewport_w
        and y + h <= camera.viewport_y + camera.viewport_h
    )


def preview_patterns(is_ctrl_held: bool, grid: PastePattern, pattern_name: str | None, camera: Camera) -> tuple[pygame.Surface, tuple[int, int]]:
    """Preview selected patterns and show if you can paste it."""
    pos = pygame.mouse.get_pos()
    pattern = grid.preview(pattern_name, cell_size=camera.cell_size) if is_ctrl_held else grid.preview(cell_size=camera.cell_size)
    color = settings.PASTE_ON if is_inside_viewport(pos, pattern, camera) else settings.PASTE_OFF
    pattern = (
        grid.preview(pattern_name, cell_size=camera.cell_size, color=color) if is_ctrl_held else grid.preview(cell_size=camera.cell_size, color=color)
    )
    return pattern, pos


def viewport_center(camera: Camera) -> tuple[int, int]:
    """Return the screen center of the viewport."""
    return (
        camera.viewport_x + camera.viewport_w // 2,
        camera.viewport_y + camera.viewport_h // 2,
    )


def toggle_fullscreen(is_fullscreen: bool) -> tuple[bool, pygame.Surface]:
    """Change to fullscreen mode."""
    flags = 0 if is_fullscreen else FULLSCREEN
    screen = pygame.display.set_mode(settings.WINDOW_SIZE, flags)

    return not is_fullscreen, screen


def toggle_modal(grid: PastePattern, modal: bool, paused: bool) -> bool:
    """Open or close the modal."""
    modal = not modal

    # Pause everything when modal is activated and
    # start everything when modal is inactivated, but
    # only if the board already was started.
    if modal and grid.generation and not paused:
        grid.stop()

    if not modal and grid.generation and not paused:
        grid.start()

    return modal


def handle_control_action(
    action: str,
    grid: PastePattern,
    is_paused: bool,
    is_finished: bool,
) -> tuple[bool, bool]:
    """Dispatch a media control button action. Returns updated (is_paused, is_finished)."""
    if action == "rewind":
        grid.direction = "backward"
        is_finished = False

    elif action == "skip_back":
        grid.step_back()
        is_finished = False

    elif action == "play_pause":
        if grid.run:
            grid.stop()
            is_paused = True
        elif get_cell_count(grid) or grid.history:
            grid.start()
            is_paused = False
            is_finished = False

    elif action == "stop":
        grid.reset()
        is_paused = False
        is_finished = False

    elif action == "skip_forward":
        grid.step_forward()
        is_finished = False

    elif action == "fast_forward":
        grid.direction = "forward"
        is_finished = False

    return is_paused, is_finished
