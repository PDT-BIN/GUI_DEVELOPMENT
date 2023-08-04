import calendar
import datetime

from canvas import *


def get_date_components():
    today = datetime.datetime.today()
    day, month = today.day, today.month
    weekday = calendar.day_name[today.weekday()]
    match day % 10:
        case 1:
            suffix = 'st'
        case 2:
            suffix = 'nd'
        case 3:
            suffix = 'rd'
        case _:
            suffix = 'th'
    return day, weekday, suffix, month


# TEMPERATURE.
class SimplePanel(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, data: dict, row_index: int, column_index: int, color: dict,
                 animations: list):
        super().__init__(
            master=parent, fg_color=color['main'], corner_radius=0)
        self.grid(row=row_index, column=column_index, sticky=ctk.NSEW)
        # LAYOUT.
        self.rowconfigure(0, weight=1, uniform='A')
        self.columnconfigure((0, 1), weight=1, uniform='A')
        # COMPONENT.
        temperature = ctk.CTkFrame(master=self, fg_color='transparent')
        ctk.CTkLabel(master=temperature, text_color=color['text'],
                     text=f'{data["temp"]}\N{DEGREE SIGN}',
                     font=('Cambria', 50, 'bold')).pack()
        ctk.CTkLabel(master=temperature, text_color=color['text'],
                     text=f'Feels like: {data["feels_like"]}\N{DEGREE SIGN}',
                     font=('Rockwell', 16)).pack()
        temperature.grid(row=0, column=0)
        AnimatedImage(self, 0, 1, animations, color['main'])


# LOCATION & DATE.
class DatePanel(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, data: dict, row_index: int, column_index: int, color: dict):
        super().__init__(
            master=parent, fg_color=color['main'], corner_radius=0)
        self.grid(row=row_index, column=column_index, sticky=ctk.NSEW)
        # LOCATION.
        location = ctk.CTkFrame(master=self, fg_color='transparent')
        ctk.CTkLabel(master=location, text_color=color['text'],
                     text=f'{data["city"]} ', font=('Rockwell', 16, 'bold')).pack(side=ctk.LEFT)
        ctk.CTkLabel(master=location, text_color=color['text'],
                     text=f'({data["country"]})', font=('Rockwell', 16)).pack(side=ctk.LEFT)
        location.pack(side=ctk.LEFT, padx=10)
        # DATE.
        day, weekday, suffix, month = get_date_components()
        ctk.CTkLabel(master=self, fg_color='transparent', text_color=color['text'],
                     text=f'{weekday[:3]}, {day}{suffix} {calendar.month_name[month]}',
                     font=('Rockwell', 16)).pack(side=ctk.RIGHT, padx=10)


# TEMPERATURE & DATE HORIZONTALLY.
class HorizontalForecastPanel(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, data: dict, row_index: int, column_index: int,
                 rowspan: int, color: str, forecast_graphic: list):
        super().__init__(master=parent, fg_color='#FFF', corner_radius=0)
        self.grid(row=row_index, column=column_index,
                  rowspan=rowspan, sticky=ctk.NSEW, padx=6, pady=6)
        # COMPONENT.
        for index, (key, value) in enumerate(data.items()):
            forecast = ctk.CTkFrame(master=self, fg_color='transparent')
            # LAYOUT.
            forecast.columnconfigure(0, weight=1, uniform='A')
            forecast.rowconfigure(0, weight=5, uniform='A')
            forecast.rowconfigure(1, weight=2, uniform='A')
            forecast.rowconfigure(2, weight=1, uniform='A')
            # COMPONENT.
            StaticImage(forecast, forecast_graphic[index], 0, 0)
            weekday = calendar.day_name[calendar.weekday(
                *map(lambda e: int(e), str.split(key, '-')))][:3]
            ctk.CTkLabel(master=forecast, text_color='#444', font=('Cambria', 18, 'bold'),
                         text=f'{value["temp"]}\N{DEGREE SIGN}').grid(column=0, row=1, sticky=ctk.N)
            ctk.CTkLabel(master=forecast, text_color='#444', font=('Rockwell', 16),
                         text=weekday).grid(column=0, row=2)
            forecast.pack(side=ctk.LEFT, expand=True,
                          fill=ctk.BOTH, padx=5, pady=5)
            if index < len(data) - 1:
                ctk.CTkFrame(master=self, width=2, fg_color=color).pack(
                    side=ctk.LEFT, fill=ctk.BOTH)


# LOCATION & DATE & TEMPERATURE.
class SimpleTallPanel(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, weather_data: dict, location_data: dict,
                 row_index: int, column_index: int, color: dict, animations: list):
        super().__init__(
            master=parent, fg_color=color['main'], corner_radius=0)
        self.grid(row=row_index, column=column_index, sticky=ctk.NSEW)
        # LAYOUT.
        self.columnconfigure(0, weight=1, uniform='A')
        self.rowconfigure((0, 2, 4), weight=1, uniform='A')
        self.rowconfigure(1, weight=2, uniform='A')
        self.rowconfigure((3, 5), weight=6, uniform='A')
        # LOCATION & DATE.
        information = ctk.CTkFrame(master=self, fg_color='transparent')
        day, weekday, suffix, month = get_date_components()
        ctk.CTkLabel(master=information, text_color=color['text'],
                     text=f'{weekday[:3]}, {day}{suffix} {calendar.month_name[month]}',
                     font=('Rockwell', 16)).pack(side=ctk.BOTTOM)
        ctk.CTkLabel(master=information, text_color=color['text'],
                     text=f'{location_data["city"]} ',
                     font=('Rockwell', 16, 'bold')).pack(side=ctk.LEFT)
        ctk.CTkLabel(master=information, text_color=color['text'],
                     text=f'({location_data["country"]})',
                     font=('Rockwell', 16)).pack(side=ctk.LEFT)
        information.grid(column=0, row=1, padx=5, pady=5)
        # GRAPHIC.
        AnimatedImage(self, 3, 0, animations, color['main'])
        # TEMPERATURE.
        temperature = ctk.CTkFrame(master=self, fg_color='transparent')
        ctk.CTkLabel(master=temperature, text_color=color['text'],
                     text=f'{weather_data["temp"]}\N{DEGREE SIGN}',
                     font=('Cambria', 50, 'bold')).pack()
        ctk.CTkLabel(master=temperature, text_color=color['text'],
                     text=f'Feels like: {weather_data["feels_like"]}\N{DEGREE SIGN}',
                     font=('Rockwell', 16)).pack()
        temperature.grid(row=5, column=0)


# TEMPERATURE & DATE VERTICALLY.
class VerticalForecastPanel(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, data: dict, row_index: int, column_index: int,
                 color: str, forecast_graphic: list):
        super().__init__(master=parent, fg_color='#FFF', corner_radius=0)
        self.grid(row=row_index, column=column_index,
                  sticky=ctk.NSEW, padx=6, pady=6)
        # COMPONENT.
        for index, (key, value) in enumerate(data.items()):
            forecast = ctk.CTkFrame(master=self, fg_color='transparent')
            # LAYOUT.
            forecast.rowconfigure(0, weight=1, uniform='A')
            forecast.columnconfigure((0, 1, 2, 3), weight=1, uniform='A')
            # COMPONENT.
            weekday = calendar.day_name[calendar.weekday(
                *map(lambda e: int(e), str.split(key, '-')))]
            ctk.CTkLabel(master=forecast, text_color='#444', font=('Rockwell', 16),
                         text=weekday).grid(row=0, column=0, sticky=ctk.E)
            ctk.CTkLabel(master=forecast, text_color='#444', font=('Cambria', 18, 'bold'),
                         text=f'{value["temp"]}\N{DEGREE SIGN}').grid(row=0, column=2, sticky=ctk.E, padx=5)
            StaticImage(forecast, forecast_graphic[index], 0, 3)
            forecast.pack(expand=True, fill=ctk.BOTH, padx=5, pady=5)
            if index < len(data) - 1:
                ctk.CTkFrame(
                    master=self, height=2, fg_color=color).pack(fill=ctk.BOTH)
