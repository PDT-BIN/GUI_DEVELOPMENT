import customtkinter as ctk
from menu import Menu
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageTk
from settings import *
from widgets import CloseEditor, ImageEditor, ImageLoader


class Application(ctk.CTk):
    def __init__(self):
        # SET-UP.
        super().__init__()
        ctk.set_appearance_mode('DARK')
        self.center_window(1000, 600)
        self.title('Photoshop')
        self.minsize(800, 500)
        self.binding_data()
        # CANVAS DATA.
        self.image_width = self.image_height = 0
        self.canvas_width = self.canvas_height = 0
        # LAYOUT.
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3, uniform='A')
        self.columnconfigure(1, weight=7, uniform='A')
        # WIDGET.
        self.loader = ImageLoader(self, self.load_image)

    def center_window(self, width: int, height: int):
        self.geometry(f'{width}x{height}' +
                      f'+{(self.winfo_screenwidth() - width) // 2}' +
                      f'+{(self.winfo_screenheight() - height) // 2}')

    def binding_data(self):
        # BINDING.
        self.binding_source: dict[str, dict[str, ctk.Variable]] = {
            'POSITION': {
                'ROTATE': ctk.DoubleVar(value=DEFAULT_ROTATE),
                'ZOOM': ctk.DoubleVar(value=DEFAULT_ZOOM),
                'FLIP': ctk.StringVar(value=FLIP_OPTIONS[0])
            },
            'COLOUR': {
                'BRIGHTNESS': ctk.DoubleVar(value=DEFAULT_BRIGHTNESS),
                'GRAYSCALE': ctk.BooleanVar(value=DEFAULT_GRAYSCALE),
                'INVERT': ctk.BooleanVar(value=DEFAULT_INVERT),
                'VIBRANCE': ctk.DoubleVar(value=DEFAULT_VIBRANCE)
            },
            'EFFECT': {
                'BLUR': ctk.DoubleVar(value=DEFAULT_BLUR),
                'CONTRAST': ctk.IntVar(value=DEFUALT_CONTRAST),
                'EFFECT': ctk.StringVar(value=EFFECT_OPTIONS[0])
            }
        }
        # TRACING.
        for data_source in self.binding_source.values():
            for binding_data in data_source.values():
                binding_data.trace(ctk.W, self.manipulate_image)

    def manipulate_image(self, *args):
        self.image = self.original.copy()
        # ROTATE.
        if (value := self.binding_source['POSITION']['ROTATE'].get()) != DEFAULT_ROTATE:
            self.image = self.image.rotate(value)
        # ZOOM.
        if (value := self.binding_source['POSITION']['ZOOM'].get()) != DEFAULT_ZOOM:
            self.image = ImageOps.crop(self.image, value)
        # FLIP.
        match self.binding_source['POSITION']['FLIP'].get():
            case 'NONE':
                pass
            case 'X':
                self.image = ImageOps.mirror(self.image)
            case 'Y':
                self.image = ImageOps.flip(self.image)
            case 'BOTH':
                self.image = ImageOps.mirror(self.image)
                self.image = ImageOps.flip(self.image)
        # BRIGHTNESS.
        if (value := self.binding_source['COLOUR']['BRIGHTNESS'].get()) != DEFAULT_BRIGHTNESS:
            ENHANCER = ImageEnhance.Brightness(self.image)
            self.image = ENHANCER.enhance(value)
        # VIBRANCE.
        if (value := self.binding_source['COLOUR']['VIBRANCE'].get()) != DEFAULT_VIBRANCE:
            ENHANCER = ImageEnhance.Color(self.image)
            self.image = ENHANCER.enhance(value)
        # GRAYSCALE.
        if self.binding_source['COLOUR']['GRAYSCALE'].get():
            self.image = ImageOps.grayscale(self.image)
        # INVERT.
        if self.binding_source['COLOUR']['INVERT'].get():
            self.image = ImageOps.invert(self.image)
        # BLUR.
        if (value := self.binding_source['EFFECT']['BLUR'].get()) != DEFAULT_BLUR:
            self.image = self.image.filter(ImageFilter.GaussianBlur(value))
        # CONSTRAST.
        if (value := self.binding_source['EFFECT']['CONTRAST'].get()) != DEFUALT_CONTRAST:
            self.image = self.image.filter(ImageFilter.UnsharpMask(value))
        # EFFECTS.
        match self.binding_source['EFFECT']['EFFECT'].get():
            case 'NONE':
                pass
            case 'EMBOSS':
                self.image = self.image.filter(ImageFilter.EMBOSS)
            case 'FIND EDGES':
                self.image = self.image.filter(ImageFilter.FIND_EDGES)
            case 'CONTOUR':
                self.image = self.image.filter(ImageFilter.CONTOUR)
            case 'EDGE ENHANCE':
                self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        # SHOW FINAL.
        self.show_image()

    def load_image(self, path: str):
        self.original = Image.open(path)
        self.image = self.original.copy()
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_ratio = self.image.width / self.image.height
        # HIDE THE IMAGE LOADER.
        self.loader.grid_forget()
        # OPEN THE IMAGE EDITOR.
        self.menu = Menu(self, self.binding_source, self.save_image)
        self.editor = ImageEditor(self, self.resize_image)
        self.closer = CloseEditor(self, self.close_editor)

    def resize_image(self, event):
        # CURRENT RATIO.
        canvas_ratio = event.width / event.height
        # GET NEW WIDTH & HEIGHT OF IMAGE & CANVAS.
        self.canvas_width = event.width
        self.canvas_height = event.height
        if canvas_ratio > self.image_ratio:
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)
        # SHOW IMAGE.
        self.show_image()

    def show_image(self):
        # CUSTOMIZED IMAGE.
        self.image_tk = ImageTk.PhotoImage(
            self.image.resize((self.image_width, self.image_height)))
        # DISCARD BEFORE DRAW.
        self.editor.delete(ctk.ALL)
        self.editor.create_image(
            self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk)

    def close_editor(self):
        # HIDE THE IMAGE EDITOR.
        self.menu.grid_forget()
        self.editor.grid_forget()
        self.closer.place_forget()
        # OPEN THE IMAGE LOADER.
        self.loader = ImageLoader(self, self.load_image)

    def save_image(self, file_path: str, file_name: str, extension: str):
        self.image.save(f'{file_path}/{file_name}.{extension}')


if __name__ == '__main__':
    Application().mainloop()
