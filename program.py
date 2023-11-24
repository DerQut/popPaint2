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

    for element in paint_layer.elements:
        if element.type == "TextField":
            element.center_text()

    cursor.pos = (mouse_pos[0]-paint_layer.x_cord, mouse_pos[1]-paint_layer.y_cord)

    if paint_layer.button.is_highlighted:
        cursor.paint()
        input_layer.draw()


def button_handler(down, event_key, needs_shifting, is_shifting):

    if down:
        print(event_key)
        if event_key == pygame.K_PERCENT:
            cursor.pos_buffer = cursor.pos
        elif 10 >= event_key >= 0:
            cursor.tool = event_key

        elif event_key == pygame.K_DELETE:
            if len(paint_layer.elements):
                print(paint_layer.elements.pop())
        elif event_key == pygame.K_F1:
            cursor.colour = parser.get_colour(cursor.colour)
        elif event_key == pygame.K_RETURN:
            filename = parser.save_file()
            if filename:
                pygame.image.save(paint_layer.pg_surface, filename)

    else:
        if event_key == pygame.K_PERCENT:
            cursor.finish()


program_window = window.Window(1280, 720, DOUBLEBUF, assets.bg_colour, "Paint")


paint_layer = paint.PaintingSurface(program_window, 0, 0, 1280, 720, (255, 255, 255))
paint_layer.button = ui_elements.Button(paint_layer, 80, 0, paint_layer.x_size-80, paint_layer.y_size, paint_layer.colour, pygame.K_PERCENT, paint_layer.colour, False, False)
cursor = paint.Cursor(paint_layer, (0, 0, 0))


input_layer = window.Surface(program_window, 0, 0, 80, 720, assets.bg_colour_inactive)

pencil_button = ui_elements.LabelledButton(input_layer, 0, 0, 40, 40, assets.blue, 1, assets.dark_blue, "Line", assets.text_colour, assets.SF_Pro_Light_16, 0)
rect_button = ui_elements.LabelledButton(input_layer, 40, 0, 40, 40, assets.blue, 2, assets.dark_blue, "Rect", assets.text_colour, assets.SF_Pro_Light_16, 0)
ellipse_button = ui_elements.LabelledButton(input_layer, 0, 40, 40, 40, assets.blue, 3, assets.dark_blue, "Ellipse", assets.text_colour, assets.SF_Pro_Light_16, 0)
text_button = ui_elements.LabelledButton(input_layer, 40, 40, 40, 40, assets.blue, 4, assets.dark_blue, "Text", assets.text_colour, assets.SF_Pro_Light_16, 0)
none_button = ui_elements.LabelledButton(input_layer, 0, 80, 40, 40, assets.blue, 0, assets.dark_blue, "None", assets.text_colour, assets.SF_Pro_Light_16, 0)
