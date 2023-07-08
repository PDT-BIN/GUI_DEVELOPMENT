from collections.abc import Callable
from tkinter import Canvas, filedialog

import customtkinter as ctk
from pyparsing import Any
from settings import *


class ImageLoader(ctk.CTkFrame):
    def __init__(self, parent, load_image: Callable[[str], None]):
        super().__init__(master=parent)
        self.grid(column=0, row=0, columnspan=2, sticky=ctk.NSEW)
        self.load_image = load_image
        # WIDGET.
        ctk.CTkButton(self, text='Open Image', command=self.open_dialog, height=45, font=ctk.CTkFont(
            'Cambria', 20, 'bold', 'italic')).place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def open_dialog(self):
        path = filedialog.askopenfilename()
        self.load_image(path)


class ImageEditor(Canvas):
    def __init__(self, parent, show_image: Callable[[Any], None]):
        super().__init__(master=parent, background=CANVAS_BG,
                         bd=0, highlightthickness=0, relief=ctk.RIDGE)
        self.grid(row=0, column=1, sticky=ctk.NSEW, padx=10, pady=10)
        self.bind('<Configure>', show_image)


class CloseEditor(ctk.CTkButton):
    def __init__(self, parent, command: Callable[[], None]):
        font = ctk.CTkFont('Ravie', 20, weight='bold')
        super().__init__(master=parent, width=50, height=50, text='X', text_color=WHITE, font=font,
                         fg_color='transparent', hover_color=CLOSE_RED, command=command)
        self.place(relx=0.99, rely=0.01, anchor=ctk.NE)
