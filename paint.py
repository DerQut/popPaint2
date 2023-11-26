import pygame

import assets
import ui_elements
import window

NONE = 0
LINE = 1
RECT = 2
ELLIPSE = 3
TEXT = 4


def get_pg_rect(pos1, pos2, left_wall, right_wall, top_wall, bottom_wall):
    x1 = pos1[0]
    y1 = pos1[1]

    x2 = pos2[0]
    y2 = pos2[1]

    top = max(min(y1, y2), top_wall)
    left = max(min(x1, x2), left_wall)

    bottom = min(max(y1, y2), bottom_wall)
    right = min(max(x1, x2), right_wall)

    width = abs(right - left)
    height = abs(bottom - top)

    rect = pygame.rect.Rect(left, top, width, height)

    return rect


class PaintingSurface(window.Surface):

    def __init__(self, window, x_cord, y_cord, x_size, y_size, colour):
        super().__init__(window, x_cord, y_cord, x_size, y_size, colour)

        self.button = ui_elements.Button(self, 0, 0, x_size-x_cord, y_size-y_cord, colour, pygame.K_PERCENT, colour, False, False)


class Cursor:

    def __init__(self, painting_surface, colour):

        self.tool = NONE

        self.colour = colour
        self.backup_colour = (255, 255, 255)

        self.pos = (0, 0)

        self.pos_buffer = (0, 0)

        self.thickness = 5
        self.width = 5

        self.font_size = 18
        self.font_name = "assets/SFPRODISPLAYMEDIUM.OTF"
        self.font = pygame.font.Font(self.font_name, self.font_size)

        self.painting_surface = painting_surface

    def paint(self):
        if self.tool == LINE:
            pygame.draw.line(self.painting_surface.window.screen, self.colour, (self.pos_buffer[0]+self.painting_surface.x_cord, self.pos_buffer[1]+self.painting_surface.y_cord), (self.pos[0]+self.painting_surface.x_cord, self.pos[1]+self.painting_surface.y_cord), self.thickness)
        elif self.tool == RECT:
            pygame.draw.rect(self.painting_surface.window.screen, self.colour, get_pg_rect((self.pos[0]+self.painting_surface.x_cord, self.pos[1]+self.painting_surface.y_cord), (self.pos_buffer[0]+self.painting_surface.x_cord, self.pos_buffer[1]+self.painting_surface.y_cord), 0, self.painting_surface.window.x_size, 0, self.painting_surface.window.y_size), self.width)
        elif self.tool == ELLIPSE:
            pygame.draw.ellipse(self.painting_surface.window.screen, self.colour, get_pg_rect((self.pos[0] + self.painting_surface.x_cord, self.pos[1] + self.painting_surface.y_cord), (self.pos_buffer[0] + self.painting_surface.x_cord, self.pos_buffer[1] + self.painting_surface.y_cord), 0, self.painting_surface.window.x_size, 0, self.painting_surface.window.y_size), self.width)
        elif self.tool == TEXT:
            pygame.draw.rect(self.painting_surface.window.screen, self.backup_colour, get_pg_rect((self.pos[0]+self.painting_surface.x_cord, self.pos[1]+self.painting_surface.y_cord), (self.pos_buffer[0]+self.painting_surface.x_cord, self.pos_buffer[1]+self.painting_surface.y_cord), 0, self.painting_surface.window.x_size, 0, self.painting_surface.window.y_size), self.width)

    def finish(self):
        rect = get_pg_rect(self.pos, self.pos_buffer, 0, self.painting_surface.x_size, 0, self.painting_surface.y_size)

        if self.tool == LINE:
            self.painting_surface.elements.append(ui_elements.Line(self.painting_surface, self.pos_buffer, self.pos, self.thickness, self.colour))
            self.painting_surface.elements.pop()

        elif self.tool == RECT:
            self.painting_surface.elements.append(ui_elements.Rect(self.painting_surface, rect.left, rect.top, rect.width, rect.height, self.colour, width=self.width))
            self.painting_surface.elements.pop()

        elif self.tool == ELLIPSE:
            self.painting_surface.elements.append(ui_elements.Ellipse(self.painting_surface, rect.left, rect.top, rect.width, rect.height, self.colour, width=self.width))
            self.painting_surface.elements.pop()

        elif self.tool == TEXT:
            new = ui_elements.TextField(self.painting_surface, rect.left, rect.top, rect.width, rect.height, self.backup_colour, "Text", self.colour, self.font, 128, self.width, (pygame.K_a, pygame.K_z), [pygame.K_SPACE])
            new.is_highlighted = True
            self.painting_surface.elements.append(new)
            self.painting_surface.elements.pop()

        for surface in self.painting_surface.window.surfaces:
            surface.draw()

    def swap_colours(self):
        buffer = self.colour
        self.colour = self.backup_colour
        self.backup_colour = buffer

    def render_font(self):
        self.font = pygame.font.Font(self.font_name, self.font_size)
