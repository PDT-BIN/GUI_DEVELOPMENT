import customtkinter as ctk
from PIL import Image, ImageTk


class StaticImage(ctk.CTkCanvas):
    def __init__(self, parent: ctk.CTkFrame, image: Image.Image, row_index: int, column_index: int):
        super().__init__(master=parent, background='WHITE', width=100, height=100,
                         bd=0, highlightthickness=0, relief=ctk.RIDGE)
        self.grid(row=row_index, column=column_index, sticky=ctk.NSEW)
        # COMPONENT.
        self.image = image
        self.image_ratio = self.image.width / self.image.height
        self.image_tk = ImageTk.PhotoImage(image)
        # START VALUE.
        self.canvas_width = self.canvas_height = 0
        self.image_width = self.image_height = 0
        # EVENT.
        self.bind('<Configure>', self.resize)

    def resize(self, event):
        canvas_ratio = event.width / event.height
        self.canvas_width = event.width
        self.canvas_height = event.height
        # FILL THE IMAGE IN CANVAS.
        if canvas_ratio > self.image_ratio:
            self.image_height = int(self.canvas_height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(self.canvas_width)
            self.image_height = int(self.image_width / self.image_ratio)
        self.update_image()

    def update_image(self):
        self.delete('all')
        resized_image = self.image.resize(
            (self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.create_image(
            self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk)


class AnimatedImage(ctk.CTkCanvas):
    def __init__(self, parent: ctk.CTkFrame, row_index: int, column_index: int,
                 animations: list[Image.Image], color: str):
        super().__init__(master=parent, background=color,
                         bd=0, highlightthickness=0, relief=ctk.RIDGE)
        self.grid(row=row_index, column=column_index, sticky=ctk.NSEW)
        # GRAPHIC.
        self.animations = animations
        self.image_index = 0
        # COMPONENT.
        image = self.animations[self.image_index]
        self.image_ratio = image.width / image.height
        self.image_tk = ImageTk.PhotoImage(image)
        # START VALUE.
        self.canvas_width = self.canvas_height = 0
        self.image_width = self.image_height = 0
        # EVENT.
        self.bind('<Configure>', self.resize)

    def animate(self):
        self.image_index += 1
        if self.image_index >= len(self.animations):
            self.image_index = 0
        self.update_image()
        self.after(42, self.animate)

    def resize(self, event):
        canvas_ratio = event.width / event.height
        self.canvas_width = event.width
        self.canvas_height = event.height
        # FILL THE IMAGE IN CANVAS.
        if canvas_ratio > self.image_ratio:
            self.image_height = int(self.canvas_height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(self.canvas_width)
            self.image_height = int(self.image_width / self.image_ratio)
        self.animate()

    def update_image(self):
        self.delete('all')
        resized_image = self.animations[self.image_index].resize(
            (self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.create_image(
            self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk)
