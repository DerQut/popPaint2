import math

import paint
import parser
import ui_elements
import window
import assets
import macos_ui

import pygame
from pygame.locals import *


def loop_action():

    mouse_pos = pygame.mouse.get_pos()

    cursor.pos = (mouse_pos[0]-paint_layer.x_cord, mouse_pos[1]-paint_layer.y_cord)

    if paint_layer.button.is_highlighted:
        cursor.paint()
        input_layer.draw()


def button_handler(down, event_key, needs_shifting, is_shifting):

    if down:
        print(event_key)
        if event_key == pygame.K_PERCENT:
            cursor.pos_buffer = cursor.pos
        elif event_key == 0:
            cursor.tool = paint.LINE
        elif event_key == 1:
            cursor.tool = paint.RECT

        elif event_key == pygame.K_DELETE:
            paint_layer.elements.pop()
        elif event_key == pygame.K_F1:
            parser.get_colour()

    else:
        if event_key == pygame.K_PERCENT:
            cursor.finish()


program_window = window.Window(1280, 720, DOUBLEBUF, assets.bg_colour, "The Graphing Engine")


input_layer = window.Surface(program_window, 0, 0, 80, 720, assets.bg_colour_inactive)
pencil_button = ui_elements.LabelledButton(input_layer, 0, 0, 40, 40, assets.blue, 0, assets.dark_blue, "Line", assets.text_colour, assets.SF_Pro_Light_16, 0)
brush_button = ui_elements.LabelledButton(input_layer, 40, 0, 40, 40, assets.blue, 1, assets.dark_blue, "Rect", assets.text_colour, assets.SF_Pro_Light_16, 0)


paint_layer = paint.PaintingSurface(program_window, 80, 0, 1200, 720, (255, 255, 255))
cursor = paint.Cursor(paint_layer, (0, 0, 0))
