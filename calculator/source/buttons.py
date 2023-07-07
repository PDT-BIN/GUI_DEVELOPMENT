from collections.abc import Callable

from customtkinter import CTkButton, CTkFont, CTkImage
from settings import *


class Button(CTkButton):
    def __init__(self, parent, text: str, column_index: int, row_index: int, font: CTkFont,
                 command: Callable[[], None], color='dark-gray', column_span: int = 1):
        super().__init__(master=parent, font=font, text=text, corner_radius=STYLE['corner-radius'],
                         fg_color=COLORS[color]['fg'], hover_color=COLORS[color]['hover'],
                         text_color=COLORS[color]['text'], command=command)
        self.grid(column=column_index, row=row_index, columnspan=column_span, sticky='NEWS',
                  padx=STYLE['gap'], pady=STYLE['gap'])


class NumberButton(Button):
    def __init__(self, parent, text: str, column_index: int, row_index: int, font: CTkFont,
                 column_span: int, command: Callable[[str], None], color='light-gray'):
        super().__init__(parent, text, column_index, row_index,
                         font, lambda: command(text), color, column_span)


class MathButton(Button):
    def __init__(self, parent, character: str, operator: str, column_index: int, row_index: int, font: CTkFont,
                 command: Callable[[str], None], color='orange', column_span: int = 1):
        super().__init__(parent, character, column_index, row_index,
                         font, lambda: command(operator), color, column_span)


class ImageButton(CTkButton):
    def __init__(self, parent, text: str, column_index: int, row_index: int, image: CTkImage,
                 command: Callable[[], None], color='dark-gray'):
        super().__init__(master=parent, image=image, text=text, corner_radius=STYLE['corner-radius'],
                         fg_color=COLORS[color]['fg'], hover_color=COLORS[color]['hover'],
                         text_color=COLORS[color]['text'], command=command)
        self.grid(column=column_index, row=row_index, sticky='NEWS',
                  padx=STYLE['gap'], pady=STYLE['gap'])


class MathImageButton(ImageButton):
    def __init__(self, parent, character: str, operator: str, column_index: int, row_index: int, image: CTkImage,
                 command: Callable[[str], None], color='orange'):
        super().__init__(parent, character, column_index,
                         row_index, image, lambda: command(operator), color)
