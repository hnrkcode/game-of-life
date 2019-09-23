import sys

import pygame
from pygame import locals

from gameoflife import settings
from gameoflife.pattern import menu, paste
from gameoflife.util import text
from gameoflife.board import Board


class MainClass:
    def __init__(self):

        # Initialize display screen.
        pygame.init()
        pygame.display.set_caption("GAME OF LIFE")
        pygame.display.set_icon(pygame.image.load(settings.ICON_FILE))
        self.size = (settings.WIDTH, settings.HEIGHT)
        self.screen = pygame.display.set_mode(self.size)

        self.fullscreen = False
        self.mouse_down = False
        self.left_ctrl_held = False
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

        self.info_text = self.format(self.info)
        self.info_group = pygame.sprite.RenderUpdates(
            self.header, self.info_text
        )

        self.board = Board()
        self.bg_group = pygame.sprite.RenderUpdates(self.board)

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

    def event_handler(self, event):
        """Handles the events triggered by the user."""

        # Exit the program.
        if (
            event.type == locals.QUIT
            or event.type == locals.KEYDOWN
            and event.key == locals.K_ESCAPE
        ):
            self.exit()

        elif event.type == locals.KEYDOWN:
            # Press enter to start the simulation.
            if event.key == locals.K_RETURN:
                self.grid.start()
            # Press R to clear the screen.
            if event.key == locals.K_r:
                self.grid.reset()
            # Press P to stop the simulation temporarily.
            if event.key == locals.K_p:
                self.grid.stop()
            # Press F11 to toggle to fullscreen mode.
            if event.key == locals.K_F11:
                self.toggle_fullscreen()
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
            if event.key == locals.K_LCTRL:
                self.left_ctrl_held = True

        elif event.type == locals.KEYUP:
            if event.key == locals.K_LCTRL:
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

        while True:

            # Control the frame rate.
            self.clock.tick(settings.FPS)

            # Handel user inputs.
            for event in pygame.event.get():
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

            for key in self.grid.cell.keys():
                if self.grid.cell[key] == 1:
                    pygame.draw.rect(
                        self.screen,
                        self.grid.cell_sprite[key].color,
                        self.grid.cell_sprite[key],
                    )

            pygame.display.update()


def main():
    gameoflife = MainClass()
    gameoflife.main()


if __name__ == "__main__":
    main()
