from components import *


class SmallWidget(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, today_data: dict, location: dict, color: dict,
                 today_animations: list):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill=ctk.BOTH)
        # LAYOUT.
        self.rowconfigure(0, weight=6, uniform='A')
        self.rowconfigure(1, weight=1, uniform='A')
        self.columnconfigure(0, weight=1, uniform='A')
        # COMPONENT.
        SimplePanel(self, today_data, 0, 0, color, today_animations)
        DatePanel(self, location, 1, 0, color)


class WideWidget(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, today_data: dict, forecast_data: dict, location: dict,
                 color: dict, forecast_graphic: list, today_animations: list):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill=ctk.BOTH)
        # LAYOUT.
        self.rowconfigure(0, weight=6, uniform='A')
        self.rowconfigure(1, weight=1, uniform='A')
        self.columnconfigure(0, weight=1, uniform='A')
        self.columnconfigure(1, weight=2, uniform='A')
        # COMPONENT.
        SimplePanel(self, today_data, 0, 0, color, today_animations)
        DatePanel(self, location, 1, 0, color)
        HorizontalForecastPanel(
            self, forecast_data, 0, 1, 2, color['divider color'], forecast_graphic)


class TallWidget(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, today_data: dict, forecast_data: dict, location: dict,
                 color: dict, forecast_graphic: list, today_animations: list):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill=ctk.BOTH)
        # LAYOUT.
        self.rowconfigure(0, weight=3, uniform='A')
        self.rowconfigure(1, weight=1, uniform='A')
        self.columnconfigure(0, weight=1, uniform='A')
        # COMPONENT.
        SimpleTallPanel(
            self, today_data, location, 0, 0, color, today_animations)
        HorizontalForecastPanel(
            self, forecast_data, 1, 0, 1, color['divider color'], forecast_graphic)


class MaxWidget(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, today_data: dict, forecast_data: dict, location: dict,
                 color: dict, forecast_graphic: list, today_animations: list):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill=ctk.BOTH)
        # LAYOUT.
        self.rowconfigure(0, weight=1, uniform='A')
        self.columnconfigure((0, 1), weight=1, uniform='A')
        # COMPONENT.
        SimpleTallPanel(
            self, today_data, location, 0, 0, color, today_animations)
        VerticalForecastPanel(
            self, forecast_data, 0, 1, color['divider color'], forecast_graphic)
