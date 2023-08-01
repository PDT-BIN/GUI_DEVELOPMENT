import customtkinter as ctk
from canvas import Canvas
from settings import *
from tool import ToolPanel


class Application(ctk.CTk):
    def __init__(self):
        # WINDOW SET-UP.
        ctk.set_appearance_mode('LIGHT')
        super().__init__()
        self.geometry('800x600')
        self.iconbitmap('paint/image/empty.ico')
        self.title('')
        # DATA.
        self.color = ctk.StringVar(value=COLORS[0][0])
        self.brush = ctk.DoubleVar(value=0.2)
        self.erase = ctk.BooleanVar()
        # DRAW VIEW.
        self.canvas = Canvas(self, self.color, self.brush, self.erase)
        ToolPanel(self, self.color, self.brush, self.erase,
                  lambda: self.canvas.delete('all'))
        # BRUSH CHOICE DEFAULT.
        self.erase.set(False)
        # EVENT.
        self.bind('<MouseWheel>', self.resize_brush)

    def resize_brush(self, event):
        # GET NEW SIZE.
        size = self.brush.get() + 0.05 * event.delta / abs(event.delta)
        # CONSTRAINT SIZE.
        size = max(0.2, min(1, size))
        # SET SIZE.
        self.brush.set(size)


if __name__ == '__main__':
    Application().mainloop()
