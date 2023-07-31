from collections.abc import Callable

import customtkinter as ctk
from PIL import Image
from settings import *


class SidePanel(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, set_style: Callable[[str], None], update_map: Callable[[str], None]):
        super().__init__(master=parent, fg_color=SIDE_PANEL_BG)
        self.grid(row=0, column=0, sticky=ctk.NSEW)
        # VIEW BUTTONS.
        ViewButtons(self, set_style)
        # VIEW HISTORY.
        self.history = ViewHistory(self, update_map)


class ViewButtons(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, set_style: Callable[[str], None]):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(side=ctk.BOTTOM, fill=ctk.BOTH, padx=5, pady=5)
        # LAYOUT.
        self.rowconfigure(0, weight=1, uniform='B')
        self.columnconfigure((0, 1, 2), weight=1, uniform='B')
        # COMPONENT.
        MAP_IMAGE = ctk.CTkImage(Image.open(
            MAP_IMAGE_PATH), Image.open(MAP_IMAGE_PATH))
        PAINT_IMAGE = ctk.CTkImage(Image.open(
            PAINT_IMAGE_PATH), Image.open(PAINT_IMAGE_PATH))
        TERRAIN_IMAGE = ctk.CTkImage(Image.open(
            TERRAIN_IMAGE_PATH), Image.open(TERRAIN_IMAGE_PATH))
        ctk.CTkButton(master=self, text='', width=60, height=35, image=MAP_IMAGE,
                      fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR,
                      command=lambda: set_style('MAIN')).grid(row=0, column=0, sticky=ctk.W)
        ctk.CTkButton(master=self, text='', width=60, height=35, image=TERRAIN_IMAGE,
                      fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR,
                      command=lambda: set_style('TERRAIN')).grid(row=0, column=1)
        ctk.CTkButton(master=self, text='', width=60, height=35, image=PAINT_IMAGE,
                      fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR,
                      command=lambda: set_style('PAINT')).grid(row=0, column=2, sticky=ctk.E)


class ViewHistory(ctk.CTkScrollableFrame):
    def __init__(self, parent: ctk.CTkFrame, update_map: Callable[[str], None]):
        self.update_map = update_map
        super().__init__(master=parent)
        self.pack(expand=True, fill=ctk.BOTH, padx=5, pady=5)
        # FONT.
        self.font = ctk.CTkFont(TEXT_FONT, TEXT_SIZE - 2)

    def add_location(self, location: str):
        HistoryItem(self, location, self.font, self.update_map)


class HistoryItem(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkScrollableFrame, location, font: ctk.CTkFont,
                 update_map: Callable[[str], None]):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(fill=ctk.X)
        # DATA.
        areas = str.split(location.address, ', ')
        town, country = areas[0], areas[-1]
        address = country if town == country else f'{town}, {country}'
        # BUTTONS.
        ctk.CTkButton(master=self, anchor=ctk.W, text=address, text_color=TEXT_COLOR,
                      fg_color='transparent', hover_color=HISTORY_HOVER_COLOR, font=font,
                      command=lambda: update_map(address)).pack(side=ctk.LEFT)
        ctk.CTkButton(master=self, anchor=ctk.CENTER, width=30, text='X', text_color=TEXT_COLOR,
                      fg_color='transparent', hover_color=HISTORY_HOVER_COLOR, font=font,
                      command=lambda: self.pack_forget()).pack(side=ctk.RIGHT)
