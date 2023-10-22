import math
import os

import pygame
from pygame.locals import (
    FULLSCREEN,
    K_DOWN,
    K_ESCAPE,
    K_F11,
    K_LCTRL,
    K_RCTRL,
    K_RETURN,
    K_UP,
    KEYDOWN,
    KEYUP,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    QUIT,
    K_h,
    K_p,
    K_r,
)

from gameoflife import settings
from gameoflife.board import Board
from gameoflife.modal import Modal, Overlay, ScreenText
from gameoflife.pattern.menu import ScrollMenu
from gameoflife.pattern.paste import PastePattern
from gameoflife.util.text import InfoText


def main():
    """Main function that contains the game loop."""

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

    # Initialize menu and board variables.
    grid = PastePattern()
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
        [
            settings.WIDTH / 2 - (splash_header.image.get_width() / 2),
            settings.HEIGHT / 3,
        ]
    )

    splash_start = InfoText(
        "Press to start",
        size=settings.H2,
    )

    splash_start.set_position(
        [
            settings.WIDTH / 2 - (splash_start.image.get_width() / 2),
            settings.HEIGHT / 1.75,
        ]
    )

    splash_screen_group = pygame.sprite.RenderUpdates(splash_header, splash_start)

    # Layout the text on the left side of the board.
    sidebar_layout = (
        [
            InfoText("INFORMATION", size=settings.H3),
            InfoText(f"Generation: {grid.generation}", size=settings.TEXT),
            InfoText(f"Cells: {get_cell_count(grid)}", size=settings.TEXT),
            InfoText(f"Total deaths: {grid.deaths}", size=settings.TEXT),
            InfoText(f"Grid: {settings.TOTAL_CELLS}", size=settings.TEXT),
            InfoText(f"FPS: {clock.get_fps():.1f}", size=settings.TEXT),
            InfoText(None, size=settings.TEXT),
        ]
        + scroll_menu.format("PATTERNS", pattern_name, menu_obj)
        + [
            InfoText(None, size=settings.TEXT),
            InfoText("HELP", size=settings.H3),
            InfoText("Press (H) for help", size=settings.TEXT),
        ]
    )

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

    # Update pause text intervall.
    pygame.time.set_timer(pygame.USEREVENT, 200)

    while True:
        # Control the frame rate.
        clock.tick(settings.FPS)
        screen.fill(settings.BG_COLOR)

        # Handel user inputs.
        for event in pygame.event.get():
            # Exit the program.
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return

            # Press F11 to toggle to fullscreen mode.
            elif event.type == KEYDOWN and event.key == K_F11:
                is_fullscreen, screen = toggle_fullscreen(is_fullscreen)

            # Events captured only while splash screen is running.
            if is_splash_screen:
                if event.type == pygame.USEREVENT:
                    splash_start.rect[1] = (
                        settings.HEIGHT / 1.75 + int(5 * math.sin(splash_start_num)) + 5
                    )
                    splash_start_num += 1

                # Press any keyboard key or mouse button to close splash screen and start game.
                elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
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
                elif (
                    event.type == pygame.USEREVENT
                    and not get_cell_count(grid)
                    and grid.generation
                ):
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
                        if event.key == K_p:
                            # Can only pause if there are cells and the generation is more than zero.
                            if is_pausable(grid):
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
                        if event.key == K_LCTRL or event.key == K_RCTRL:
                            is_ctrl_held = True

                    elif event.type == KEYUP and (
                        event.key == K_LCTRL or event.key == K_RCTRL
                    ):
                        is_ctrl_held = False

                    # Scroll through patterns.
                    elif (
                        event.type == MOUSEBUTTONDOWN
                        and event.button == settings.SCROLL_DOWN
                    ):
                        grid.select.next()
                        pattern_name, paste_pattern = grid.select.get_current()
                        menu_obj = scroll_menu.setup(grid.select)

                    elif (
                        event.type == MOUSEBUTTONDOWN
                        and event.button == settings.SCROLL_UP
                    ):
                        grid.select.previous()
                        pattern_name, paste_pattern = grid.select.get_current()
                        menu_obj = scroll_menu.setup(grid.select)

                    # Left click to deploy cells or right click to remove cells.
                    elif event.type == MOUSEBUTTONDOWN:
                        if is_finished:
                            grid.reset()
                            is_paused, is_finished = False, False

                        is_mouse_held = True

                    elif event.type == MOUSEBUTTONUP:
                        is_mouse_held = False

        if is_splash_screen:
            splash_screen_group.draw(screen)
        else:
            # Draw/erase cells on the grid.
            if is_mouse_held:
                pos = pygame.mouse.get_pos()
                button = pygame.mouse.get_pressed()

                if is_ctrl_held:
                    paste_pattern(name=pattern_name, pos=pos, button=button)
                else:
                    paste_pattern(pos=pos, button=button)

            # Update the grid.
            if grid.run:
                grid.update()

            # Update runtime information.
            sidebar_text[1].update(f"Generation: {grid.generation}")
            sidebar_text[2].update(f"Cells: {get_cell_count(grid)}")
            sidebar_text[3].update(f"Total deaths: {grid.deaths}")
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
            preview = preview_patterns(is_ctrl_held, grid, pattern_name)
            screen.blit(*preview)

            for key in grid.cell.keys():
                if grid.cell[key] == 1:
                    pygame.draw.rect(
                        screen,
                        grid.cell_sprite[key].color,
                        grid.cell_sprite[key],
                    )

            if is_paused:
                pause_screen_group.draw(screen)

            # Show end screen when there are no more cells left on the board.
            if has_finished(grid):
                grid.stop()
                end_screen_group.draw(screen)
                is_finished = True
                is_paused = False

            if is_modal_active:
                modal_group.draw(screen)

        pygame.display.update()


def format_sidebar(lines):
    """Arrange the sidebars text lines on the screen."""

    x, y = 30, settings.BOARD_Y_POS

    for line in lines:
        line.set_position((x, y))
        # Add different vertical space depending on font size.
        y = (y + 40) if line.fontsize > settings.TEXT else (y + 20)

    return lines


def get_cell_count(grid):
    """Return number alive cells on the grid."""

    return len(grid.cell_sprite)


def has_finished(grid):
    """Returns true when atleast one generation has passed and all cells are dead."""

    if not get_cell_count(grid) and grid.generation > 0:
        return True

    return False


def is_pausable(grid):
    """Check if the game can be paused."""

    # Can only pause when there are alive cells and
    if get_cell_count(grid) and grid.generation > 0:
        return True

    return False


def preview_patterns(is_ctrl_held, grid, pattern_name):
    """Preview selected patterns and show if you can paste it."""

    pos = pygame.mouse.get_pos()

    if is_ctrl_held:
        pattern = grid.preview(pos, pattern_name)
    else:
        pattern = grid.preview(pos)

    return pattern, pos


def toggle_fullscreen(is_fullscreen):
    """Change to fullscreen mode."""

    if is_fullscreen:
        screen = pygame.display.set_mode(settings.WINDOW_SIZE)
    else:
        screen = pygame.display.set_mode(settings.WINDOW_SIZE, FULLSCREEN)

    return (not is_fullscreen, screen)


def toggle_modal(grid, modal, paused):
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
