import pygame

import assets
import ui_elements
import window

LINE = 1
RECT = 2
ELLIPSE = 3
TEXT = 4


def get_pg_rect(pos1, pos2):

    x1 = pos1[0]
    y1 = pos1[1]

    x2 = pos2[0]
    y2 = pos2[1]

    top = min(y1, y2)
    left = min(x1, x2)

    width = abs(x1-x2)
    height = abs(y1-y2)

    rect = pygame.rect.Rect(left, top, width, height)

    return rect


class PaintingSurface(window.Surface):

    def __init__(self, window, x_cord, y_cord, x_size, y_size, colour):
        super().__init__(window, x_cord, y_cord, x_size, y_size, colour)

        self.button = None


class Cursor:

    def __init__(self, painting_surface, colour):

        self.tool = LINE

        self.colour = colour
        self.backup_colour = (10, 10, 10)

        self.pos = (0, 0)

        self.pos_buffer = (0, 0)

        self.thickness = 5

        self.painting_surface = painting_surface

    def paint(self):
        if self.tool == LINE:
            pygame.draw.line(self.painting_surface.window.screen, self.colour, (self.pos_buffer[0]+self.painting_surface.x_cord, self.pos_buffer[1]+self.painting_surface.y_cord), (self.pos[0]+self.painting_surface.x_cord, self.pos[1]+self.painting_surface.y_cord), self.thickness)
        elif self.tool == RECT:
            pygame.draw.rect(self.painting_surface.window.screen, self.colour, get_pg_rect((self.pos[0]+self.painting_surface.x_cord, self.pos[1]+self.painting_surface.y_cord), (self.pos_buffer[0]+self.painting_surface.x_cord, self.pos_buffer[1]+self.painting_surface.y_cord)))
        elif self.tool == ELLIPSE:
            pygame.draw.ellipse(self.painting_surface.window.screen, self.colour, get_pg_rect((self.pos[0] + self.painting_surface.x_cord, self.pos[1] + self.painting_surface.y_cord), (self.pos_buffer[0] + self.painting_surface.x_cord, self.pos_buffer[1] + self.painting_surface.y_cord)))
        elif self.tool == TEXT:
            pygame.draw.rect(self.painting_surface.window.screen, self.colour, get_pg_rect((self.pos[0]+self.painting_surface.x_cord, self.pos[1]+self.painting_surface.y_cord), (self.pos_buffer[0]+self.painting_surface.x_cord, self.pos_buffer[1]+self.painting_surface.y_cord)), 5)

    def finish(self):
        rect = get_pg_rect(self.pos, self.pos_buffer)

        if self.tool == LINE:
            self.painting_surface.elements.append(ui_elements.Line(self.painting_surface, self.pos_buffer, self.pos, self.thickness, self.colour))

        elif self.tool == RECT:
            self.painting_surface.elements.append(ui_elements.Rect(self.painting_surface, rect.left, rect.top, rect.width, rect.height, self.colour))

        elif self.tool == ELLIPSE:
            self.painting_surface.elements.append(ui_elements.Ellipse(self.painting_surface, rect.left, rect.top, rect.width, rect.height, self.colour))

        elif self.tool == TEXT:
            new = ui_elements.TextField(self.painting_surface, rect.left, rect.top, rect.width, rect.height, self.backup_colour, "Text", self.colour, assets.SF_Pro_Medium_18, 128, (pygame.K_a, pygame.K_z), [pygame.K_SPACE])
            new.is_highlighted = True
            self.painting_surface.elements.append(new)

        self.painting_surface.elements.pop()

        for surface in self.painting_surface.window.surfaces:
            surface.draw()
