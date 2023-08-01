from customtkinter import BOTH, RIDGE, ROUND, CTk, CTkCanvas, Variable
from settings import *


class Canvas(CTkCanvas):
    def __init__(self, parent: CTk, color_variable: Variable, brush_variable: Variable,
                 erase_tool_variable: Variable):
        # LINK.
        self.color = color_variable
        self.brush = brush_variable
        self.erase_tool = erase_tool_variable
        self.allow_draw = False
        self.old_x = self.old_y = None
        # SET-UP.
        super().__init__(master=parent, background=CANVS_BG,
                         bd=0, highlightthickness=0, relief=RIDGE)
        self.pack(expand=True, fill=BOTH)
        # EVENT.
        self.bind('<Motion>', self.draw)
        self.bind('<Button>', self.activate)
        self.bind('<ButtonRelease>', self.deactivate)

    def activate(self, event):
        self.allow_draw = True
        self.line((event.x, event.y), (event.x + 1, event.y + 1))

    def deactivate(self, event):
        self.allow_draw = False
        self.old_x = self.oldy = None

    def draw(self, event):
        if self.allow_draw:
            if self.old_x and self.old_y:
                self.line((self.old_x, self.old_y), (event.x, event.y))
            self.old_x, self.old_y = event.x, event.y

    def line(self, src: tuple, des: tuple):
        width = self.brush.get() * 10 ** 2
        color = f'#{self.color.get()}' if not self.erase_tool.get() else '#FFF'
        self.create_line(src, des, width=width, capstyle=ROUND, fill=color)
