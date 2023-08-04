# URL REQUEST.
# import json
# import urllib.request

from os import walk

import customtkinter as ctk
from PIL import Image
from settings import *
from weather_data import get_weather
from windows import MaxWidget, SmallWidget, TallWidget, WideWidget

try:
    from ctypes import byref, c_int, sizeof, windll
except:
    pass


class Application(ctk.CTk):
    def __init__(self, city: str, country: str, today_data: dict, forecast_data: dict):
        # DATA.
        self.today, self.forecast = today_data, forecast_data
        self.location = {'city': city, 'country': country}
        self.color = WEATHER_DATA[today_data['weather']]
        # GRAPHIC.
        self.forecast_graphic = [
            Image.open(f'weather/image/symbols/{data["weather"]}.png')
            for data in forecast_data.values()]
        self.today_animations = self.import_image_folder(self.color['path'])
        # WINDOW SET-UP.
        super().__init__(fg_color=self.color['main'])
        self.color_title_bar(self.color['title'])
        self.geometry('600x250')
        self.minsize(600, 250)
        self.iconbitmap('weather/image/empty.ico')
        self.title('')
        # RESPONSIVE WINDOW.
        self.window = SmallWidget(
            self, self.today, self.location, self.color, self.today_animations)
        self.WIDTH_BREAK = 1375
        self.HEIGHT_BREAK = 600
        self.break_width = ctk.BooleanVar(value=False)
        self.break_height = ctk.BooleanVar(value=False)
        self.bind('<Configure>', self.check_responsive)
        self.break_width.trace('w', self.update_window)
        self.break_height.trace('w', self.update_window)

    @staticmethod
    def import_image_folder(path: str):
        for _, _, files in walk(path):
            return [Image.open(f'{path}/{file}') for file in files]

    def color_title_bar(self, color: str):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(
                HWND, 35, byref(c_int(color)), sizeof(c_int))
        except:
            pass

    def check_responsive(self, event):
        if event.widget == self:
            # CHECK WIDTH BREAK.
            if self.break_width.get():
                if event.width < self.WIDTH_BREAK:
                    self.break_width.set(False)
            else:
                if event.width > self.WIDTH_BREAK:
                    self.break_width.set(True)
            # CHECK HEIGHT BREAK.
            if self.break_height.get():
                if event.height < self.HEIGHT_BREAK:
                    self.break_height.set(False)
            else:
                if event.height > self.HEIGHT_BREAK:
                    self.break_height.set(True)

    def update_window(self, *args):
        # DELETE THE PREVIOUS WINDOW.
        self.window.pack_forget()
        # MAX WIDGET.
        if self.break_width.get() and self.break_height.get():
            self.window = MaxWidget(self, self.today, self.forecast, self.location, self.color,
                                    self.forecast_graphic, self.today_animations)
        # WIDE WIDGET.
        if self.break_width.get() and not self.break_height.get():
            self.window = WideWidget(self, self.today, self.forecast, self.location, self.color,
                                     self.forecast_graphic, self.today_animations)
        # TALL WIDGET.
        if not self.break_width.get() and self.break_height.get():
            self.window = TallWidget(self, self.today, self.forecast, self.location, self.color,
                                     self.forecast_graphic, self.today_animations)
        # SMALL WIDGET.
        if not self.break_width.get() and not self.break_height.get():
            self.window = SmallWidget(
                self, self.today, self.location, self.color, self.today_animations)


if __name__ == '__main__':
    # LOCATION INFORMATION.
    # with urllib.request.urlopen('https://ipapi.co/json/') as url:
    #     location_data = json.loads(url.read().decode())
    #     city = location_data['city']
    #     country = location_data['country']
    #     latitude = location_data['latitude']
    #     longitude = location_data['longitude']
    CITY = 'TP. Hồ Chí Minh'
    COUNTRY = 'Việt Nam'
    LATITUDE = 10.762622
    LONGITUDE = 106.660172
    # WEATHER INFORMATION.
    TODAY_DATA = get_weather(LATITUDE, LONGITUDE, 'metric', 'today')
    FORECAST_DATA = get_weather(LATITUDE, LONGITUDE, 'metric', 'forecast')
    # RUN APP.
    Application(CITY, COUNTRY, TODAY_DATA, FORECAST_DATA).mainloop()
