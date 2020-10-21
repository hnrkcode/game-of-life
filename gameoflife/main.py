import sys

import pygame
from pygame import locals

from gameoflife import settings
from gameoflife.board import Board
from gameoflife.pattern import menu, paste
from gameoflife.util import text

from gameoflife.modal import Modal, Overlay, Pause, End

class MainClass:
    def __init__(self):

        # Initialize display screen.
        pygame.init()
        pygame.display.set_caption("GAME OF LIFE")
        pygame.display.set_icon(pygame.image.load(settings.ICON_FILE))
        self.size = (settings.WIDTH, settings.HEIGHT)
        self.screen = pygame.display.set_mode(self.size)

        self.is_finished = False
        self.fullscreen = False
        self.mouse_down = False
        self.left_ctrl_held = False
        self.paused = False
        self.clock = pygame.time.Clock()
        self.grid = paste.PastePattern()
        self.name, self.func = self.grid.select.get_current()
        self.menu = menu.ScrollMenu()
        self.menu_obj = self.menu.setup(self.grid.select)

        self.h1 = 35
        self.h2 = 25
        self.p = 15

        self.header_pos = (settings.BOARD_WIDTH_SIZE / 1.6, 0)
        self.header = text.InfoText(
            "GAME OF LIFE",
            self.h1,
            pos=self.header_pos,
            font=settings.HEADER_FONT,
        )

        self.info = [
            text.InfoText("INFORMATION", self.h2),
            text.InfoText(f"Generation: {self.grid.generation}", self.p),
            text.InfoText(f"Cells: {len(self.grid.cell_sprite)}", self.p),
            text.InfoText(f"Total deaths: {self.grid.deaths}", self.p),
            text.InfoText(f"Grid: {settings.TOTAL_CELLS}", self.p),
            text.InfoText(f"FPS: {self.clock.get_fps():.1f}", self.p),
            text.InfoText(None, self.p),
        ] + self.menu.format("PATTERNS", self.name, self.menu_obj)

        self.info += [
            text.InfoText(None, self.p),
            text.InfoText("HELP", self.h2),
            text.InfoText("Press (H) for help", self.p)
        ]

        self.info_text = self.format(self.info)
        self.info_group = pygame.sprite.RenderUpdates(
            self.header, self.info_text
        )

        self.board = Board()
        self.bg_group = pygame.sprite.RenderUpdates(self.board)

        self.modal = Modal()
        self.overlay = Overlay()
        self.modal_group = pygame.sprite.RenderUpdates(self.overlay, self.modal)
        self.active_modal = False

        self.pause_screen = Pause()
        self.pause_group = pygame.sprite.RenderUpdates(self.pause_screen)

        self.end = End()
        self.end_group = pygame.sprite.RenderUpdates(self.end)

    def format(self, information):
        """Arrange the information text on the screen."""

        x, y = 30, settings.BOARD_Y_POS

        for info in information:
            if info.fontsize > self.p:
                info.set_position((x, y))
                y += 40
            else:
                info.set_position((x, y))
                y += 20

        return information

    def exit(self):
        """Exit the game of life simulator."""

        sys.exit()

    def toggle_fullscreen(self):
        """Change to fullscreen mode."""

        if self.fullscreen:
            self.fullscreen = False
            self.screen = pygame.display.set_mode(self.size)
        else:
            self.fullscreen = True
            self.screen = pygame.display.set_mode(self.size, locals.FULLSCREEN)

    def preview_patterns(self):
        """Preview selected patterns and show if you can paste it."""

        pos = pygame.mouse.get_pos()
        pattern = self.grid.preview(self.name, pos)
        self.screen.blit(pattern, pos)
    
    def reset_game(self):
        """Reset game to default values."""

        self.grid.reset()
        self.paused = False
        self.is_finished = False

    def event_handler(self, event):
        """Handles the events triggered by the user."""

        if event.type == locals.KEYDOWN:
            # Press enter to start the simulation.
            if event.key == locals.K_RETURN:
                # Can only start if there are any cells on the board.
                if len(self.grid.cell_sprite):
                    self.grid.start()
                    self.paused = False
            # Press R to clear the screen.
            if event.key == locals.K_r:
                self.reset_game()
            # Press P to stop the simulation temporarily.
            if event.key == locals.K_p:
                # Can only pause if there are cells and the generation is more than zero.
                if len(self.grid.cell_sprite) and self.grid.generation:
                    if self.paused:
                        self.grid.start()
                    else:
                        self.grid.stop()
                    self.paused = not self.paused
            # Choose predefined pattern.
            if event.key == locals.K_UP:
                self.grid.select.previous()
                self.name, self.func = self.grid.select.get_current()
                self.menu_obj = self.menu.setup(self.grid.select)
            if event.key == locals.K_DOWN:
                self.grid.select.next()
                self.name, self.func = self.grid.select.get_current()
                self.menu_obj = self.menu.setup(self.grid.select)
            # Hold left control button to paste pattern when left clicking.
            if event.key == locals.K_LCTRL or event.key == locals.K_RCTRL:
                self.left_ctrl_held = True

        elif event.type == locals.KEYUP:
            if event.key == locals.K_LCTRL or event.key == locals.K_RCTRL:
                self.left_ctrl_held = False

        # Scroll through patterns.
        elif (
            event.type == locals.MOUSEBUTTONDOWN
            and event.button == settings.SCROLL_DOWN
        ):
            self.grid.select.next()
            self.name, self.func = self.grid.select.get_current()
            self.menu_obj = self.menu.setup(self.grid.select)

        elif (
            event.type == locals.MOUSEBUTTONDOWN
            and event.button == settings.SCROLL_UP
        ):
            self.grid.select.previous()
            self.name, self.func = self.grid.select.get_current()
            self.menu_obj = self.menu.setup(self.grid.select)

        # Left click to deploy cells or right click to remove cells.
        elif event.type == locals.MOUSEBUTTONDOWN:

            if self.is_finished:
                self.reset_game()

            cursor_pos = pygame.mouse.get_pos()
            mouse_button = pygame.mouse.get_pressed()
            # Paste predefined patterns.
            if self.left_ctrl_held and mouse_button == settings.LEFT_CLICK:
                self.func(cursor_pos, self.name)
            else:
                # Hold mouse button to draw or erase without clicking.
                self.mouse_down = True

        elif event.type == locals.MOUSEBUTTONUP:
            self.mouse_down = False

    def main(self):
        """Main method of the program."""

        # Update pause text intervall.
        pygame.time.set_timer(pygame.USEREVENT, 200)

        while True:

            # Control the frame rate.
            self.clock.tick(settings.FPS)

            # Handel user inputs.
            for event in pygame.event.get():
                # Update pause text.
                if event.type == pygame.USEREVENT and self.paused:
                    self.pause_group.update()
                
                if event.type == pygame.USEREVENT and not len(self.grid.cell_sprite) and self.grid.generation:
                    self.end_group.update()

                # Exit the program.
                elif (
                    event.type == locals.QUIT
                    or event.type == locals.KEYDOWN
                    and event.key == locals.K_ESCAPE
                ):
                    self.exit()

                # Press F11 to toggle to fullscreen mode.
                elif event.type == locals.KEYDOWN and event.key == locals.K_F11:
                    self.toggle_fullscreen()

                # Toggle modal.
                elif event.type == locals.KEYDOWN and event.key == locals.K_h:
                    self.active_modal = not self.active_modal
                    
                    # Pause everything when modal is activated and
                    # start everything when modal is inactivated, but
                    # only if the board already was started.
                    if self.active_modal and self.grid.generation and not self.paused:
                        self.grid.stop()
                    
                    if not self.active_modal and self.grid.generation and not self.paused:
                        self.grid.start()
                
                # User can only interact with the board when the modal isn't active.
                if not self.active_modal:
                    self.event_handler(event)

            # Draw/erase cells on the grid.
            if self.mouse_down:
                position = pygame.mouse.get_pos()
                button = pygame.mouse.get_pressed()
                self.grid.change_status(position, button)

            # Update the grid.
            if self.grid.run:
                self.grid.update()

            # Update runtime information.
            self.info_text[1].update(f"Generation: {self.grid.generation}")
            self.info_text[2].update(f"Cells: {len(self.grid.cell_sprite)}")
            self.info_text[3].update(f"Total deaths: {self.grid.deaths}")
            self.info_text[5].update(f"FPS: {self.clock.get_fps():.1f}")

            # Update pattern scroll menu.
            self.menu.update(self.info_text, self.menu_obj, self.name, 8, 19)

            # Draw everything to the screen.
            self.screen.fill(settings.BG_COLOR)
            self.info_group.draw(self.screen)
            self.bg_group.draw(self.screen)

            # Preview selected pattern.
            if self.left_ctrl_held:
                self.preview_patterns()

            for key in self.grid.cell.keys():
                if self.grid.cell[key] == 1:
                    pygame.draw.rect(
                        self.screen,
                        self.grid.cell_sprite[key].color,
                        self.grid.cell_sprite[key],
                    )
            
            if self.paused:
                self.pause_group.draw(self.screen)

            # Show end screen when there are no more cells left on the board.
            if not len(self.grid.cell_sprite) and self.grid.generation:
                self.grid.stop()
                self.end_group.draw(self.screen)
                self.is_finished = True

            if self.active_modal:
                self.modal_group.draw(self.screen)

            pygame.display.update()


def main():
    gameoflife = MainClass()
    gameoflife.main()


if __name__ == "__main__":
    main()
