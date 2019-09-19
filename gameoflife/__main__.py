import sys

import pygame
from pygame import locals

from gameoflife import settings
from gameoflife.pattern import paste
from gameoflife.util import text


class MainClass:
    def __init__(self):
        pygame.init()
        self.size = (settings.WIDTH, settings.HEIGHT)
        self.screen = pygame.display.set_mode(self.size)

        self.fullscreen = False
        self.mouse_down = False
        self.left_ctrl_held = False
        self.clock = pygame.time.Clock()
        self.cell = paste.PastePattern()
        self.name, self.func = self.cell.select.get_current()

        pygame.display.set_caption("GAME OF LIFE")
        pygame.display.set_icon(pygame.image.load(settings.ICON_FILE))

        self.h1 = 35
        self.h2 = 25
        self.p = 15

        self.header_pos = (settings.BOARD_WIDTH_SIZE / 1.6, 0)
        self.header = (
            text.InfoText(
                self.h1,
                "GAME OF LIFE",
                pos=self.header_pos,
                font=settings.HEADER,
            ),
        )

        self.info = [
            text.InfoText(self.h2, "INFORMATION"),
            text.InfoText(self.p, f"Generation: {self.cell.generation}"),
            text.InfoText(self.p, f"Living cells: {self.cell.living}"),
            text.InfoText(self.p, f"Total deaths: {self.cell.deaths}"),
            text.InfoText(self.p, f"Grid: {settings.TOTAL_CELLS}"),
            text.InfoText(self.p, f"FPS: {self.clock.get_fps():.1f}"),
            text.InfoText(self.p, f""),
            text.InfoText(self.h2, "PATTERNS"),
            text.InfoText(self.p, f"{self.name}"),
        ]
        self.info_text = self.format(self.info)
        self.info_group = pygame.sprite.RenderUpdates(
            self.header, self.info_text
        )

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
                self.cell.start()
            # Press R to clear the screen.
            if event.key == locals.K_r:
                self.cell.reset()
            # Press P to stop the simulation temporarily.
            if event.key == locals.K_p:
                self.cell.stop()
            # Press F11 to toggle to fullscreen mode.
            if event.key == locals.K_F11:
                self.toggle_fullscreen()
            # Choose predefined pattern.
            if event.key == locals.K_UP:
                self.cell.select.previous()
                self.name, self.func = self.cell.select.get_current()
            if event.key == locals.K_DOWN:
                self.cell.select.next()
                self.name, self.func = self.cell.select.get_current()
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
            self.cell.select.next()
            self.name, self.func = self.cell.select.get_current()
        elif (
            event.type == locals.MOUSEBUTTONDOWN
            and event.button == settings.SCROLL_UP
        ):
            self.cell.select.previous()
            self.name, self.func = self.cell.select.get_current()

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
                self.cell.change_status(position, button)

            # Update the grid.
            if self.cell.run:
                self.cell.update()

            # Update runtime information.
            self.info_text[1].update(f"Generation: {self.cell.generation}")
            self.info_text[2].update(f"Living cells: {self.cell.living}")
            self.info_text[3].update(f"Total deaths: {self.cell.deaths}")
            self.info_text[5].update(f"FPS: {self.clock.get_fps():.1f}")
            self.info_text[8].update(f"{self.name}")

            # Draw everything to the screen.
            self.screen.fill(settings.BG_COLOR)
            self.info_group.draw(self.screen)
            for key in self.cell.cells.keys():
                color = self.cell.cells[key].color
                cell = self.cell.cells[key]
                pygame.draw.rect(self.screen, color, cell)

            pygame.display.update()


def main():
    gameoflife = MainClass()
    gameoflife.main()


if __name__ == "__main__":
    main()
