import tkinter as tk
from collections.abc import Callable

import customtkinter as ctk
import qrcode
from PIL import ImageTk


class Application(ctk.CTk):
    def __init__(self):
        # WINDOW SET-UP.
        ctk.set_appearance_mode('LIGHT')
        super().__init__(fg_color='WHITE')
        # CUSTOMIZATION.
        self.geometry('400x400')
        self.iconbitmap('QR/empty.ico')
        self.title('')
        # ENTRY FIELD.
        self.QR_string = ctk.StringVar()
        EntryField(self, self.QR_string, self.export_QR)
        self.QR_string.trace('w', self.create_QR)
        # DISPLAY FIELD.
        self.original = self.image_tk = None
        self.QR_image = QRImage(self)
        # EXPORT EVENT.
        self.bind('<Return>', self.export_QR)

    def create_QR(self, *args):
        if string := self.QR_string.get():
            self.original = qrcode.make(string)
            self.image_tk = ImageTk.PhotoImage(self.original)
            self.QR_image.update_image(self.image_tk)
        else:
            self.QR_image.clear()
            self.original = self.image_tk = None

    def export_QR(self, event=None):
        if self.original:
            if file_path := ctk.filedialog.asksaveasfilename():
                self.original.save(file_path + '.png')


class QRImage(tk.Canvas):
    def __init__(self, parent: ctk.CTk):
        super().__init__(master=parent, background='WHITE',
                         # HIDE THE BORDER.
                         bd=0, highlightthickness=0, relief=ctk.RIDGE)
        self.place(relx=0.5, rely=0.4, width=300,
                   height=300, anchor=ctk.CENTER)

    def update_image(self, image_tk: ImageTk):
        self.clear()
        self.create_image(0, 0, image=image_tk, anchor=ctk.NW)

    def clear(self):
        self.delete(ctk.ALL)


class EntryField(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, link_variable: ctk.Variable, export_image: Callable):
        super().__init__(master=parent, corner_radius=20, fg_color='#021FB3')
        self.place(relx=0.5, rely=1, relwidth=1,
                   relheight=0.4, anchor=ctk.CENTER)
        # LAYOUT.
        self.rowconfigure((0, 1), weight=1, uniform='A')
        self.columnconfigure(0, weight=1, uniform='A')
        # CONTAINER.
        self.container = ctk.CTkFrame(master=self, fg_color='transparent')
        self.container.columnconfigure(0, weight=1, uniform='B')
        self.container.columnconfigure(1, weight=4, uniform='B')
        self.container.columnconfigure(2, weight=2, uniform='B')
        self.container.columnconfigure(3, weight=1, uniform='B')
        self.container.grid(row=0, column=0)
        # COMPONENT.
        ctk.CTkEntry(master=self.container, fg_color='#2E54E8', border_width=0, text_color='WHITE',
                     textvariable=link_variable).grid(row=0, column=1, sticky=ctk.NSEW)
        ctk.CTkButton(master=self.container, text='SAVE', fg_color='#2E54E8', hover_color='#4266F1',
                      command=export_image).grid(row=0, column=2, sticky=ctk.NSEW, padx=10)


if __name__ == '__main__':
    Application().mainloop()
