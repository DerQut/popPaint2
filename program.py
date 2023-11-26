import paint
import parser
import ui_elements
import window
import assets

import pygame
from pygame.locals import *

from tkinter import messagebox


def loop_action():

    mouse_pos = pygame.mouse.get_pos()
    main_colour_button.main_colour = cursor.colour
    main_colour_button.colour = cursor.colour
    main_colour_button.secondary_colour = cursor.colour
    backup_colour_button.main_colour = cursor.backup_colour
    backup_colour_button.secondary_colour = cursor.backup_colour
    backup_colour_button.colour = cursor.backup_colour

    for element in paint_layer.elements:
        if element.type == "TextField":
            element.center_text()

    cursor.pos = (mouse_pos[0]-paint_layer.x_cord, mouse_pos[1]-paint_layer.y_cord)

    if paint_layer.button.is_highlighted:
        cursor.paint()
        button_layer.draw()
        button_layer.draw()


def button_handler(down, event_key, needs_shifting, is_shifting):

    if down:
        if event_key == pygame.K_PERCENT:
            cursor.pos_buffer = cursor.pos
        elif event_key == pygame.K_0:
            cursor.tool = paint.NONE
            highlight.x_cord = 0
            highlight.y_cord = 0
        elif event_key == pygame.K_1:
            cursor.tool = paint.LINE
            highlight.x_cord = 0
            highlight.y_cord = 42
        elif event_key == pygame.K_2:
            highlight.x_cord = 41
            highlight.y_cord = 42
            cursor.tool = paint.RECT
        elif event_key == pygame.K_3:
            highlight.x_cord = 82
            highlight.y_cord = 42
            cursor.tool = paint.ELLIPSE
        elif event_key == pygame.K_4:
            highlight.x_cord = 123
            highlight.y_cord = 42
            cursor.tool = paint.TEXT

        elif event_key == pygame.K_DELETE:
            if len(paint_layer.elements) > 1:
                if paint_layer.elements.pop().type == "Text":
                    paint_layer.elements.pop()
        elif event_key == pygame.K_F1:
            messagebox.showinfo("Help", """Sterowanie:

F1-  Pomoc

0- Narzędzie łapki
1- Narzędzie linii
2- Narzędzie prostokąta
3- Narzędzie elipsy
4- Narzędzie tekstu

F2-  Zmiana koloru głównego
F3-  Zmiana koloru zapasowego
F4-  Zamiana kolorów

F9-  Zmiana grubości linii
       oraz rozmiaru czcionki
       
F10- Zmiana czcionki
 
F11- Zapis do pliku
F12- Odczyt z pliku""")

        elif event_key == pygame.K_F2:
            cursor.colour = parser.get_colour(cursor.colour)
        elif event_key == pygame.K_F3:
            cursor.backup_colour = parser.get_colour(cursor.backup_colour)
        elif event_key == pygame.K_F4:
            cursor.swap_colours()

        elif event_key == pygame.K_F9:
            if cursor.tool != paint.TEXT:
                cursor.thickness = parser.get_value("Zmiana grubości pędzla", "Grubość:", cursor.thickness)
            else:
                cursor.font_size = parser.get_value("Zmiana rozmiaru czcionki", "Rozmiar:", cursor.font_size)
                cursor.render_font()

        elif event_key == pygame.K_F10:
            cursor.font_name = parser.read_file("Wybór czcionki", [("OTF Files", "*.otf")], "*.otf", "")
            cursor.render_font()

        elif event_key == pygame.K_F11:
            filename = parser.save_file()
            if filename:
                pygame.image.save(paint_layer.pg_surface, filename)

        elif event_key == pygame.K_F12:
            filename = parser.read_file()
            if filename:
                new = ui_elements.Element(paint_layer, 0, 0, pygame.image.load(filename).convert(), True)

        highlight.rect_update()
    else:
        if event_key == pygame.K_PERCENT:
            cursor.finish()


program_window = window.Window(1280, 720, DOUBLEBUF, assets.bg_colour, "Paint")


paint_layer = paint.PaintingSurface(program_window, 165, 0, 1115, 720, (255, 255, 255))
cursor = paint.Cursor(paint_layer, (0, 0, 0))

left_layer = window.Surface(program_window, 0, 0, 165, 720, assets.bg_colour_inactive)
button_layer = window.Surface(program_window, 0, 1, 165, 84, assets.dark_blue)

highlight = ui_elements.Rect(button_layer, 0, 0, 42, 42, (200, 200, 255))

none_button = ui_elements.LabelledButton(button_layer, 1, 1, 40, 40, assets.blue, pygame.K_0, assets.dark_blue, "None", assets.text_colour, assets.SF_Pro_Light_16, 0)
settings_button = ui_elements.LabelledButton(button_layer, 42, 1, 40, 40, assets.blue, pygame.K_F9, assets.dark_blue, "Settings", assets.text_colour, assets.SF_Pro_Light_16, 0)
save_button = ui_elements.LabelledButton(button_layer, 83, 1, 40, 40, assets.blue, pygame.K_F11, assets.dark_blue, "Save", assets.text_colour, assets.SF_Pro_Light_16, 0)
open_button = ui_elements.LabelledButton(button_layer, 124, 1, 40, 40, assets.blue, pygame.K_F12, assets.dark_blue, "Open", assets.text_colour, assets.SF_Pro_Light_16, 0)

line_button = ui_elements.LabelledButton(button_layer, 1, 43, 40, 40, assets.blue, pygame.K_1, assets.dark_blue, "Line", assets.text_colour, assets.SF_Pro_Light_16, 0)
rect_button = ui_elements.LabelledButton(button_layer, 42, 43, 40, 40, assets.blue, pygame.K_2, assets.dark_blue, "Rect", assets.text_colour, assets.SF_Pro_Light_16, 0)
ellipse_button = ui_elements.LabelledButton(button_layer, 83, 43, 40, 40, assets.blue, pygame.K_3, assets.dark_blue, "Ellipse", assets.text_colour, assets.SF_Pro_Light_16, 0)
text_button = ui_elements.LabelledButton(button_layer, 124, 43, 40, 40, assets.blue, pygame.K_4, assets.dark_blue, "Text", assets.text_colour, assets.SF_Pro_Light_16, 0)

backup_colour_border = ui_elements.Rect(left_layer, 58, 178, 44, 44, (64, 64, 64), True)
backup_colour_button = ui_elements.Button(left_layer, 60, 180, 40, 40, (255, 255, 255), pygame.K_F3, (255, 255, 255), False, True)
main_colour_border = ui_elements.Rect(left_layer, 38, 158, 44, 44, (64, 64, 64), True)
main_colour_button = ui_elements.Button(left_layer, 40, 160, 40, 40, (0, 0, 0), pygame.K_F2, (0, 0, 0), False, True)
colour_swap_button = ui_elements.Button(left_layer, 82, 168, 10, 10, (128, 128, 128), pygame.K_F4, (180, 180, 180), False, True)
