import math

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
from gameoflife.pattern import menu, paste
from gameoflife.util.text import InfoText


class MainClass:
    def __init__(self):

        # Initialize display screen.
        pygame.init()
        pygame.display.set_caption(settings.GAME_NAME)
        pygame.display.set_icon(pygame.image.load(settings.ICON_FILE))
        self.screen = pygame.display.set_mode(settings.WINDOW_SIZE)

        # Initialize state variables.
        self.is_running = True
        self.is_paused = False
        self.is_finished = False
        self.is_ctrl_held = False
        self.is_mouse_held = False
        self.is_fullscreen = False
        self.is_modal_active = False
        self.is_splash_screen = True

        self.number = 0
        self.clock = pygame.time.Clock()
        self.grid = paste.PastePattern()
        self.pattern_name, self.paste_pattern = self.grid.select.get_current()
        self.menu = menu.ScrollMenu()
        self.menu_obj = self.menu.setup(self.grid.select)

        # Splash screen text.
        self.splash_header = InfoText(
            settings.GAME_NAME,
            size=settings.H1,
            font=settings.HEADER_FONT,
        )

        self.splash_header.set_position(
            [
                settings.WIDTH / 2 - (self.splash_header.image.get_width() / 2),
                settings.HEIGHT / 3,
            ]
        )

        self.splash_start = InfoText(
            "Press to start",
            size=settings.H2,
        )

        self.splash_start.set_position(
            [
                settings.WIDTH / 2 - (self.splash_start.image.get_width() / 2),
                settings.HEIGHT / 1.75,
            ]
        )

        # Layout the text on the left side of the board.
        self.sidebar_layout = (
            [
                InfoText("INFORMATION", size=settings.H3),
                InfoText(f"Generation: {self.grid.generation}", size=settings.TEXT),
                InfoText(f"Cells: {self.get_cell_count()}", size=settings.TEXT),
                InfoText(f"Total deaths: {self.grid.deaths}", size=settings.TEXT),
                InfoText(f"Grid: {settings.TOTAL_CELLS}", size=settings.TEXT),
                InfoText(f"FPS: {self.clock.get_fps():.1f}", size=settings.TEXT),
                InfoText(None, size=settings.TEXT),
            ]
            + self.menu.format("PATTERNS", self.pattern_name, self.menu_obj)
            + [
                InfoText(None, size=settings.TEXT),
                InfoText("HELP", size=settings.H3),
                InfoText("Press (H) for help", size=settings.TEXT),
            ]
        )

        self.splash_screen_group = pygame.sprite.RenderUpdates(self.splash_header, self.splash_start)

        self.sidebar_text = self.format_sidebar(self.sidebar_layout)
        self.sidebar_group = pygame.sprite.RenderUpdates(self.sidebar_text)

        # Background color of the board.
        self.board = Board()
        self.board_bg_group = pygame.sprite.RenderUpdates(self.board)

        # Modal that can be toggled to show help information.
        self.modal = Modal()
        self.overlay = Overlay()
        self.modal_group = pygame.sprite.RenderUpdates(self.overlay, self.modal)

        # Is shown when the user has paused the game.
        self.pause_screen = ScreenText("PAUSE")
        self.pause_screen_group = pygame.sprite.RenderUpdates(self.pause_screen)

        # Is shown when all cells have died.
        self.end_screen = ScreenText("GAMEOVER")
        self.end_screen_group = pygame.sprite.RenderUpdates(self.end_screen)

    def format_sidebar(self, lines):
        """Arrange the sidebars text lines on the screen."""

        x, y = 30, settings.BOARD_Y_POS

        for line in lines:
            line.set_position((x, y))
            # Add different vertical space depending on font size.
            y = (y + 40) if line.fontsize > settings.TEXT else (y + 20)

        return lines

    def exit_game(self):
        """Exit the game of life simulator."""

        self.is_running = False

    def toggle_fullscreen(self):
        """Change to fullscreen mode."""

        if self.is_fullscreen:
            self.screen = pygame.display.set_mode(settings.WINDOW_SIZE)
        else:
            self.screen = pygame.display.set_mode(settings.WINDOW_SIZE, FULLSCREEN)

        self.is_fullscreen = not self.is_fullscreen

    def toggle_modal(self):
        """Open or close the modal."""

        self.is_modal_active = not self.is_modal_active

        # Pause everything when modal is activated and
        # start everything when modal is inactivated, but
        # only if the board already was started.
        if self.is_modal_active and self.grid.generation and not self.is_paused:
            self.grid.stop()

        if not self.is_modal_active and self.grid.generation and not self.is_paused:
            self.grid.start()

    def preview_patterns(self):
        """Preview selected patterns and show if you can paste it."""

        pos = pygame.mouse.get_pos()
        pattern = self.grid.preview(self.pattern_name, pos)
        self.screen.blit(pattern, pos)

    def reset_game(self):
        """Reset game to default values."""

        self.grid.reset()
        self.is_paused = False
        self.is_finished = False

    def get_cell_count(self):
        """Return number alive cells on the grid."""

        return len(self.grid.cell_sprite)

    def event_handler(self, event):
        """Handles the events triggered by the user."""

        if event.type == KEYDOWN:
            # Press enter to start the simulation.
            if event.key == K_RETURN:
                # Can only start if there are any cells on the board.
                if self.get_cell_count():
                    self.grid.start()
                    self.is_paused = False
            # Press R to clear the screen.
            if event.key == K_r:
                self.reset_game()
            # Press P to stop the simulation temporarily.
            if event.key == K_p:
                # Can only pause if there are cells and the generation is more than zero.
                if self.get_cell_count() and self.grid.generation:
                    if self.is_paused:
                        self.grid.start()
                    else:
                        self.grid.stop()
                    self.is_paused = not self.is_paused
            # Choose predefined pattern.
            if event.key == K_UP:
                self.grid.select.previous()
                self.pattern_name, self.paste_pattern = self.grid.select.get_current()
                self.menu_obj = self.menu.setup(self.grid.select)
            if event.key == K_DOWN:
                self.grid.select.next()
                self.pattern_name, self.paste_pattern = self.grid.select.get_current()
                self.menu_obj = self.menu.setup(self.grid.select)
            # Hold left control button to paste pattern when left clicking.
            if event.key == K_LCTRL or event.key == K_RCTRL:
                self.is_ctrl_held = True

        elif event.type == KEYUP:
            if event.key == K_LCTRL or event.key == K_RCTRL:
                self.is_ctrl_held = False

        # Scroll through patterns.
        elif event.type == MOUSEBUTTONDOWN and event.button == settings.SCROLL_DOWN:
            self.grid.select.next()
            self.pattern_name, self.paste_pattern = self.grid.select.get_current()
            self.menu_obj = self.menu.setup(self.grid.select)

        elif event.type == MOUSEBUTTONDOWN and event.button == settings.SCROLL_UP:
            self.grid.select.previous()
            self.pattern_name, self.paste_pattern = self.grid.select.get_current()
            self.menu_obj = self.menu.setup(self.grid.select)

        # Left click to deploy cells or right click to remove cells.
        elif event.type == MOUSEBUTTONDOWN:

            if self.is_finished:
                self.reset_game()

            cursor_pos = pygame.mouse.get_pos()
            mouse_button = pygame.mouse.get_pressed()
            # Paste predefined patterns.
            if self.is_ctrl_held and mouse_button == settings.LEFT_CLICK:
                self.paste_pattern(pattern=self.pattern_name, pos=cursor_pos)
            else:
                # Hold mouse button to draw or erase without clicking.
                self.is_mouse_held = True

        elif event.type == MOUSEBUTTONUP:
            self.is_mouse_held = False

    def has_finished(self):
        """Returns true when atleast one generation has passed and all cells are dead."""

        return not self.get_cell_count() and self.grid.generation

    def splash_screen(self):

        # Handel user inputs.
        for event in pygame.event.get():

            if event.type == pygame.USEREVENT:
                self.splash_start.rect[1] = settings.HEIGHT / 1.75 + int(5 * math.sin(self.number)) + 5
                self.number += 1

            # Exit the program.
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                self.exit_game()

            # Press F11 to toggle to fullscreen mode.
            elif event.type == KEYDOWN and event.key == K_F11:
                self.toggle_fullscreen()

            # Press any keyboard key or mouse button to close splash screen and start game.
            elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                self.is_splash_screen = False

        self.screen.fill(settings.BG_COLOR)

        self.splash_screen_group.draw(self.screen)

    def game_loop(self):
        # Handel user inputs.
        for event in pygame.event.get():
            # Update pause text.
            if event.type == pygame.USEREVENT and self.is_paused:
                self.pause_screen_group.update()

            # Update end text.
            elif (
                event.type == pygame.USEREVENT
                and not self.get_cell_count()
                and self.grid.generation
            ):
                self.end_screen_group.update()

            # Exit the program.
            elif event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                self.exit_game()

            # Press F11 to toggle to fullscreen mode.
            elif event.type == KEYDOWN and event.key == K_F11:
                self.toggle_fullscreen()

            # Toggle modal.
            elif event.type == KEYDOWN and event.key == K_h:
                self.toggle_modal()

            # User can only interact with the board when the modal isn't active.
            if not self.is_modal_active:
                self.event_handler(event)

        # Draw/erase cells on the grid.
        if self.is_mouse_held:
            position = pygame.mouse.get_pos()
            button = pygame.mouse.get_pressed()
            self.grid.change_status(position, button)

        # Update the grid.
        if self.grid.run:
            self.grid.update()

        # Update runtime information.
        self.sidebar_text[1].update(f"Generation: {self.grid.generation}")
        self.sidebar_text[2].update(f"Cells: {self.get_cell_count()}")
        self.sidebar_text[3].update(f"Total deaths: {self.grid.deaths}")
        self.sidebar_text[5].update(f"FPS: {self.clock.get_fps():.1f}")

        # Update pattern scroll menu.
        self.menu.update(
            display=self.sidebar_text,
            menu=self.menu_obj,
            active=self.pattern_name,
            start=8,
            end=19,
        )

        # Draw everything to the screen.
        self.screen.fill(settings.BG_COLOR)
        self.sidebar_group.draw(self.screen)
        self.board_bg_group.draw(self.screen)

        # Preview selected pattern.
        if self.is_ctrl_held:
            self.preview_patterns()

        for key in self.grid.cell.keys():
            if self.grid.cell[key] == 1:
                pygame.draw.rect(
                    self.screen,
                    self.grid.cell_sprite[key].color,
                    self.grid.cell_sprite[key],
                )

        if self.is_paused:
            self.pause_screen_group.draw(self.screen)

        # Show end screen when there are no more cells left on the board.
        if self.has_finished():
            self.grid.stop()
            self.end_screen_group.draw(self.screen)
            self.is_finished = True

        if self.is_modal_active:
            self.modal_group.draw(self.screen)

    def main(self):
        """Main method of the program."""

        # Update pause text intervall.
        pygame.time.set_timer(pygame.USEREVENT, 200)

        while self.is_running:

            # Control the frame rate.
            self.clock.tick(settings.FPS)

            if self.is_splash_screen:
                self.splash_screen()
            else:
                self.game_loop()

            pygame.display.update()


def main():
    gameoflife = MainClass()
    gameoflife.main()


if __name__ == "__main__":
    main()
