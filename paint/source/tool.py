from collections.abc import Callable

import customtkinter as ctk
from PIL import Image
from settings import *


class ToolPanel(ctk.CTkToplevel):
    def __init__(self, main: ctk.CTk, color_variable: ctk.Variable, brush_variable: ctk.Variable,
                 erase_variable: ctk.Variable, clear_canvas: Callable):
        super().__init__()
        self.geometry('200x300')
        self.title('')
        self.iconbitmap('paint/image/empty.ico')
        self.resizable(False, False)
        self.attributes('-topmost', True)
        self.protocol('WM_DELETE_WINDOW', main.quit)
        # LAYOUT.
        self.columnconfigure((0, 1, 2), weight=1, uniform='A')
        self.rowconfigure(0, weight=2, uniform='A')
        self.rowconfigure(1, weight=3, uniform='A')
        self.rowconfigure((2, 3), weight=1, uniform='A')
        # COMPONENT.
        ColorSliderPanel(self, color_variable, erase_variable)
        BrushPreview(self, color_variable, brush_variable, erase_variable)
        ColorPanel(self, color_variable, erase_variable)
        BrushSizeSlider(self, brush_variable)
        BrushButton(self, erase_variable)
        EraseButton(self, erase_variable)
        ClearButton(self, erase_variable, clear_canvas)


# SECTION 1.
class ColorSliderPanel(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkToplevel, color_variable: ctk.Variable, erase_variable: ctk.Variable):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky=ctk.NSEW, padx=5, pady=5)
        # DATA.
        self.color_RGB = color_variable
        self.color_R = ctk.IntVar()
        self.color_G = ctk.IntVar()
        self.color_B = ctk.IntVar()
        self.color_RGB.trace('w', self.set_color)
        self.erase = erase_variable
        # LAYOUT.
        self.rowconfigure((0, 1, 2), weight=1, uniform='A')
        self.columnconfigure(0, weight=1, uniform='A')
        # COMPONENT.
        ctk.CTkSlider(master=self, button_color=SLIDER_RED, button_hover_color=SLIDER_RED,
                      from_=0, to=15, number_of_steps=16, variable=self.color_R,
                      command=lambda value: self.set_single_color('R', value)).grid(row=0, column=0, padx=2, pady=2)
        ctk.CTkSlider(master=self, button_color=SLIDER_GREEN, button_hover_color=SLIDER_GREEN,
                      from_=0, to=15, number_of_steps=16, variable=self.color_G,
                      command=lambda value: self.set_single_color('G', value)).grid(row=1, column=0, padx=2, pady=2)
        ctk.CTkSlider(master=self, button_color=SLIDER_BLUE, button_hover_color=SLIDER_BLUE,
                      from_=0, to=15, number_of_steps=16, variable=self.color_B,
                      command=lambda value: self.set_single_color('B', value)).grid(row=2, column=0, padx=2, pady=2)

    def set_single_color(self, color: str, value: float):
        old_color = list(self.color_RGB.get())
        match color:
            case 'R':
                old_color[0] = COLOR_RANGE[int(value)]
            case 'G':
                old_color[1] = COLOR_RANGE[int(value)]
            case 'B':
                old_color[2] = COLOR_RANGE[int(value)]
        self.color_RGB.set(''.join(old_color))

    def set_color(self, *args):
        color = tuple(self.color_RGB.get())
        self.color_R.set(COLOR_RANGE.index(color[0]))
        self.color_G.set(COLOR_RANGE.index(color[1]))
        self.color_B.set(COLOR_RANGE.index(color[2]))
        self.erase.set(False)


class BrushPreview(ctk.CTkCanvas):
    def __init__(self, parent: ctk.CTkToplevel, color_variable: ctk.Variable, brush_variable: ctk.Variable,
                 erase_variable: ctk.Variable):
        super().__init__(master=parent, background=BRUSH_PREVIEW_BG,
                         bd=0, highlightthickness=0, relief=ctk.RIDGE)
        self.grid(row=0, column=1, columnspan=2, sticky=ctk.NSEW)
        # CANVAS INFORMATION.
        self.CENTER_X = self.CENTER_Y = self.MAX_RADIUS = 0
        # DATA.
        self.color = color_variable
        self.brush = brush_variable
        self.erase = erase_variable
        # EVENT.
        self.bind('<Configure>', self.load_data)
        self.color.trace('w', self.preview)
        self.brush.trace('w', self.preview)
        self.erase.trace('w', self.preview)

    def load_data(self, event):
        self.CENTER_X, self.CENTER_Y = event.width / 2, event.height / 2
        self.MAX_RADIUS = event.height / 2 * 0.8
        self.preview()

    def preview(self, *args):
        # CLEAR.
        self.delete('all')
        # REDRAW.
        radius = self.brush.get() * self.MAX_RADIUS
        color = f'#{self.color.get()}' if not self.erase.get() \
            else BRUSH_PREVIEW_BG
        outline = color if not self.erase.get() else '#000'
        self.create_oval(self.CENTER_X - radius, self.CENTER_Y - radius,
                         self.CENTER_X + radius, self.CENTER_Y + radius,
                         fill=color, outline=outline, dash=20)


# SECTION 2.
class ColorPanel(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkToplevel, color_variable: ctk.Variable, erase_variable: ctk.Variable):
        super().__init__(master=parent, fg_color='transparent')
        self.grid(row=1, column=0, columnspan=3,
                  sticky=ctk.NSEW, padx=5, pady=5)
        # LAYOUT.
        self.columnconfigure(tuple(range(COLOR_COLS)), weight=1, uniform='A')
        self.rowconfigure(tuple(range(COLOR_ROWS)), weight=1, uniform='A')
        # COMPONENT.
        for row in range(COLOR_ROWS):
            for col in range(COLOR_COLS):
                ColorButton(self, row, col, COLORS[row][col],
                            color_variable, erase_variable)


class ColorButton(ctk.CTkButton):
    def __init__(self, parent: ctk.CTkFrame, row_index: int, column_index: int, color: str,
                 color_variable: ctk.Variable, erase_variable: ctk.Variable):
        self.color = color_variable
        self.erase = erase_variable
        self.original_color = color
        super().__init__(master=parent, text='', fg_color=f'#{color}', hover_color=f'#{color}',
                         corner_radius=1, command=self.click_color)
        self.grid(row=row_index, column=column_index,
                  sticky=ctk.NSEW, padx=0.5, pady=0.5)

    def click_color(self):
        self.color.set(self.original_color)
        self.erase.set(False)


# SECTION 3.
class BrushSizeSlider(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkToplevel, link_variable: ctk.Variable):
        super().__init__(master=parent)
        self.grid(row=2, column=0, columnspan=3,
                  sticky=ctk.NSEW, padx=5, pady=5)
        # COMPONENT.
        ctk.CTkSlider(master=self, variable=link_variable, from_=0.2, to=1).pack(
            expand=True, fill=ctk.X, padx=5)


# SECTION 4.
class Button(ctk.CTkButton):
    def __init__(self, parent: ctk.CTkToplevel, image_path: str, column_index: int, command: Callable):
        image = ctk.CTkImage(Image.open(image_path), Image.open(image_path))
        super().__init__(master=parent, text='', image=image,
                         fg_color=BUTTON_COLOR, hover=BUTTON_HOVER_COLOR, command=command)
        self.grid(row=3, column=column_index, sticky=ctk.NSEW, padx=5, pady=5)


class BrushButton(Button):
    def __init__(self, parent: ctk.CTkToplevel, link_variable: ctk.Variable):
        self.erase = link_variable
        super().__init__(parent, 'paint/image/brush.png', 0, self.activate_brush)
        self.erase.trace('w', self.update_state)

    def activate_brush(self):
        self.erase.set(False)

    def update_state(self, *args):
        if not self.erase.get():
            self.configure(fg_color=BUTTON_ACTIVE_COLOR)
        else:
            self.configure(fg_color=BUTTON_COLOR)


class EraseButton(Button):
    def __init__(self, parent: ctk.CTkToplevel, link_variable: ctk.Variable):
        self.erase = link_variable
        super().__init__(parent, 'paint/image/erase.png', 1, self.activate_erase)
        self.erase.trace('w', self.update_state)

    def activate_erase(self):
        self.erase.set(True)

    def update_state(self, *args):
        if self.erase.get():
            self.configure(fg_color=BUTTON_ACTIVE_COLOR)
        else:
            self.configure(fg_color=BUTTON_COLOR)


class ClearButton(Button):
    def __init__(self, parent: ctk.CTkToplevel, link_variable: ctk.Variable, clear_canvas: Callable):
        self.erase = link_variable
        self.clear_cavas = clear_canvas
        super().__init__(parent, 'paint/image/clear.png', 2, self.activate_clear)

    def activate_clear(self):
        self.clear_cavas()
        self.erase.set(False)
