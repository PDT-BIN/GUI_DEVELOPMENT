from collections.abc import Callable

import customtkinter as ctk
import tkintermapview
from geopy.geocoders import Nominatim
from settings import *
from sidepanel import SidePanel


class Application(ctk.CTk):
    def __init__(self):
        # WINDOW SET-UP.
        ctk.set_appearance_mode('LIGHT')
        super().__init__()
        self.geometry('1200x720+100+50')
        self.minsize(800, 600)
        self.iconbitmap('map/image/logo.ico')
        self.title('Map')
        # LAYOUT.
        self.rowconfigure(0, weight=1, uniform='A')
        self.columnconfigure(0, weight=2, uniform='A')
        self.columnconfigure(1, weight=8, uniform='A')
        # DATA.
        self.keyword = ctk.StringVar()
        # MAP VIEW.
        self.map_viewer = MapView(self, self.keyword, self.submit_location)
        self.side_panel = SidePanel(
            self, self.map_viewer.set_style, self.map_viewer.set_address)

    def submit_location(self, event):
        # GET DATE.
        geolocator = Nominatim(user_agent='my-user')
        location = geolocator.geocode(self.keyword.get())
        # UPDATE MAP.
        if location:
            self.map_viewer.set_address(location.address)
            # STORE LOCATION IN SIDE PANEL.
            self.side_panel.history.add_location(location)
            # CLEAR THE LOCATION ENTRY AFTER FOUND.
            self.keyword.set('')
        else:
            self.map_viewer.location_entry.error_animation()


class MapView(tkintermapview.TkinterMapView):
    def __init__(self, parent: ctk.CTk, keyword_variable: ctk.Variable, submit_location: Callable):
        super().__init__(master=parent)
        self.grid(row=0, column=1, sticky=ctk.NSEW)
        # LOCATION ENTRY.
        self.location_entry = LocationEntry(
            self, keyword_variable, submit_location)

    def set_style(self, style: str):
        match style:
            case 'MAIN':
                self.set_tile_server(MAIN_URL)
            case 'TERRAIN':
                self.set_tile_server(TERRAIN_URL)
            case 'PAINT':
                self.set_tile_server(PAINT_URL)


class LocationEntry(ctk.CTkEntry):
    def __init__(self, parent: tkintermapview.TkinterMapView, keyword: ctk.Variable, submit: Callable):
        # ERROR ANIMATION.
        self.error_flag = False
        self.color_index = 15
        super().__init__(master=parent, width=150, fg_color=ENTRY_BG, corner_radius=0,
                         border_width=4, border_color=ENTRY_BG,
                         textvariable=keyword, text_color=TEXT_COLOR,
                         font=ctk.CTkFont(TEXT_FONT, TEXT_SIZE))
        self.place(relx=0.5, rely=0.95, anchor=ctk.CENTER)
        # EVENT.
        self.bind('<Return>', command=submit)
        keyword.trace('w', self.remove_error)

    def error_animation(self):
        self.error_flag = True
        if self.color_index > 0:
            self.color_index -= 1
            border_color = f'#F{COLOR_RANGE[self.color_index]}{COLOR_RANGE[self.color_index]}'
            text_color = f'#{COLOR_RANGE[15 - self.color_index]}00'
            self.configure(border_color=border_color, text_color=text_color)
            self.after(40, self.error_animation)

    def remove_error(self, *args):
        if self.error_flag:
            self.error_flag = False
            self.color_index = 15
            self.configure(border_color=ENTRY_BG, text_color=TEXT_COLOR)


if __name__ == '__main__':
    Application().mainloop()
