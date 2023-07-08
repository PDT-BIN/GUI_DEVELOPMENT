from collections.abc import Callable
from tkinter import filedialog
from typing import Any

import customtkinter as ctk
from settings import *


class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=DARK_GREY)
        self.pack(fill=ctk.X, padx=8, pady=4)


class SliderPanel(Panel):
    def __init__(self, parent, title: str, binding_data: ctk.Variable, minimum: int, maximum: int):
        super().__init__(parent)
        self.rowconfigure((0, 1), weight=1, uniform='B')
        self.columnconfigure((0, 1), weight=1, uniform='B')
        self.binding_data = binding_data
        self.binding_data.trace('w', self.update_output)
        # TITLE.
        ctk.CTkLabel(self, text=title, font=ctk.CTkFont(
            TITLE_FONT, 14, 'bold', 'italic')).grid(column=0, row=0, sticky=ctk.W, padx=10)
        # OUTPUT.
        self.output = ctk.CTkLabel(self, font=ctk.CTkFont(
            VALUE_FONT, 14, 'bold'), text=binding_data.get())
        self.output.grid(column=1, row=0, sticky=ctk.E, padx=10)
        # MAIN.
        ctk.CTkSlider(self, from_=minimum, to=maximum, fg_color=SLIDER_BG, variable=binding_data).grid(
            column=0, row=1, columnspan=2, sticky=ctk.EW, padx=5, pady=5)

    def update_output(self, *args):
        self.output.configure(text=f'{self.binding_data.get():.1f}')


class SegmentPanel(Panel):
    def __init__(self, parent, title: str,  binding_data: ctk.Variable, options: tuple[str]):
        super().__init__(parent)
        # TITLE.
        ctk.CTkLabel(self, text=title, font=ctk.CTkFont(
            TITLE_FONT, 14, 'bold', 'italic')).pack()
        # MAIN.
        ctk.CTkSegmentedButton(self, values=options, variable=binding_data, font=ctk.CTkFont(
            VALUE_FONT, 14, 'bold')).pack(expand=True, fill=ctk.BOTH)


class SwitchPanel(Panel):
    def __init__(self, parent, *switches: tuple[str, ctk.Variable]):
        super().__init__(parent)
        # WIDGET.
        font = ctk.CTkFont(VALUE_FONT, 14, 'bold')
        for text, data_binding in switches:
            ctk.CTkSwitch(self, text=text, variable=data_binding, button_color=BLUE,
                          fg_color=SLIDER_BG, font=font).pack(
                side=ctk.LEFT, expand=True, fill=ctk.BOTH, padx=10, pady=5)


class DropDownPanel(ctk.CTkOptionMenu):
    def __init__(self, parent, data_binding: ctk.Variable, options: tuple[str]):
        font = ctk.CTkFont(VALUE_FONT, 14, 'bold')
        super().__init__(master=parent, values=options, variable=data_binding, fg_color=DARK_GREY,
                         button_color=DROPDOWN_MAIN, button_hover_color=DROPDOWN_HOVER,
                         dropdown_fg_color=DROPDOWN_MENU, font=font, dropdown_font=font)
        self.pack(fill=ctk.X, padx=8, pady=4)


class ResetButton(ctk.CTkButton):
    def __init__(self, parent, *data_bindings: tuple[ctk.Variable, Any]):
        super().__init__(master=parent, text='RESET', command=lambda: self.update_data(data_bindings),
                         font=ctk.CTkFont(TITLE_FONT, 14, 'bold', 'italic'))
        self.pack(side=ctk.BOTTOM, pady=10)

    def update_data(self, data_bindings: tuple[ctk.Variable, Any]):
        for data_binding in data_bindings:
            data_binding[0].set(data_binding[1])


class SaveFilePanel(Panel):
    def __init__(self, parent, bds_file_name: ctk.Variable, bds_extension: ctk.Variable):
        super().__init__(parent)
        font = ctk.CTkFont(VALUE_FONT, 14, slant='italic')
        self.bds_file_name = bds_file_name
        self.bds_extension = bds_extension
        self.bds_file_name.trace('w', self.update_output)
        self.bds_extension.trace('w', self.update_output)
        # FILE NAME.
        ctk.CTkEntry(self, textvariable=bds_file_name, font=font).pack(
            fill=ctk.X, padx=20, pady=5)
        EXTENSION_FRAME = ctk.CTkFrame(self, fg_color='transparent')
        # EXTENSION.
        ctk.CTkRadioButton(EXTENSION_FRAME, text='PNG', value='png', variable=self.bds_extension,
                           radiobutton_width=10, radiobutton_height=10, border_width_checked=2,
                           border_width_unchecked=2, font=font).pack(side=ctk.LEFT, expand=True, fill=ctk.X)
        ctk.CTkRadioButton(EXTENSION_FRAME, text='JPG', value='jpg', variable=self.bds_extension,
                           radiobutton_width=10, radiobutton_height=10, border_width_checked=2,
                           border_width_unchecked=2, font=font).pack(side=ctk.LEFT, expand=True, fill=ctk.X)
        EXTENSION_FRAME.pack(expand=True, fill=ctk.X, padx=20, pady=5)
        # OUTPUT.
        self.output = ctk.CTkLabel(self, text='', font=font)
        self.output.pack(padx=20, pady=5)

    def update_output(self, *args):
        if file_name := self.bds_file_name.get():
            file = f"{file_name.replace(' ', '_')}.{self.bds_extension.get()}"
            self.output.configure(text=file)


class SavePathPanel(Panel):
    def __init__(self, parent, bds_file_path: ctk.Variable):
        super().__init__(parent)
        self.bds_file_path = bds_file_path
        # OPEN DIALOG.
        ctk.CTkButton(self, text='Open Explorer', font=ctk.CTkFont(
            VALUE_FONT, 14, 'bold'), command=self.open_dialog).pack(padx=20, pady=5)
        # OUTPUT.
        self.output = ctk.CTkEntry(self, textvariable=self.bds_file_path, font=ctk.CTkFont(
            VALUE_FONT, 12, slant='italic'))
        self.output.pack(expand=True, fill=ctk.X, padx=20, pady=5)

    def open_dialog(self):
        self.bds_file_path.set(filedialog.askdirectory())


class SaveButton(ctk.CTkButton):
    def __init__(self, parent, bds_file_name: ctk.Variable, bds_extension: ctk.Variable,
                 bds_file_path: ctk.Variable, save_image: Callable[[str, str, str], None]):
        super().__init__(master=parent, text='SAVE', command=self.download,
                         font=ctk.CTkFont(TITLE_FONT, 14, 'bold', 'italic'))
        self.pack(side=ctk.BOTTOM, pady=10)
        self.save_image = save_image
        self.bds_file_name = bds_file_name
        self.bds_extension = bds_extension
        self.bds_file_path = bds_file_path

    def download(self):
        self.save_image(self.bds_file_path.get(),
                        self.bds_file_name.get(), self.bds_extension.get())
