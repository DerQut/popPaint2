from tkinter import filedialog
from tkinter import colorchooser


def get_file():
    filename = filedialog.askopenfilename(
        filetypes=(
            ("XY files", "*.xy"),
            ("Text files", "*.txt"),
            ("Python Files", ("*.py", "*.pyx")),
            ("All Files", "*.*")
        )
    )

    return filename


def get_name(filename):

    filename_list = list(filename)
    new_list = []

    while len(filename_list):
        character = filename_list.pop()
        if character != "/" and character != "\\":
            new_list.append(character)
        else:
            break

    new_list.reverse()
    return ''.join(new_list)


def get_colour(previous_colour):
    colour_code = colorchooser.askcolor(title="Choose color", color=previous_colour)
    if bool(colour_code[0]):
        return colour_code[0]

    return previous_colour
