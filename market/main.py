from datetime import datetime

import customtkinter as ctk
import yfinance as yf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandas import DataFrame
from settings import *

try:
    from ctypes import byref, c_int, sizeof, windll
except:
    pass


class Application(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_COLOR)
        self.geometry('900x720+100+50')
        self.iconbitmap('market/empty.ico')
        self.title('')
        self.color_title_bar()
        # DATA.
        self.code = ctk.StringVar()
        self.time = ctk.StringVar()
        self.data_flag = False
        # COMPONENT.
        self.graph_panel = None
        ControlPanel(self, self.code, self.time)
        # TIME CHOICE DEFAULT.
        self.time.set(TIME_OPTIONS[0])
        # EVENT.
        self.bind('<Return>', self.get_data)
        self.time.trace('w', self.load_graph)

    def load_graph(self, *args):
        if self.graph_panel:
            self.graph_panel.pack_forget()
        if self.data_flag:
            match self.time.get():
                case '1 YEAR':
                    data = self.one_year
                case '6 MONTHS':
                    data = self.six_months
                case 'MONTH':
                    data = self.one_month
                case 'WEEK':
                    data = self.one_week
                case _:
                    data = self.all_data
            self.graph_panel = GraphPanel(self, data)

    def get_data(self, event):
        # SUCCESS FLAG.
        self.data_flag = True
        ticker = yf.Ticker(self.code.get())
        S_day = datetime(day=1, month=1, year=1950)
        E_day = datetime.today()
        # GET ALL DATA PER DAY.
        self.all_data = ticker.history(start=S_day, end=E_day, period='1d')
        # FILTER DATA.
        self.one_year = self.all_data.iloc[-260:]
        self.six_months = self.all_data.iloc[-130:]
        self.one_month = self.all_data.iloc[-22:]
        self.one_week = self.all_data.iloc[-5:]
        # LOAD DATA.
        self.load_graph()

    def color_title_bar(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(
                HWND, 35, byref(c_int(TITLE_HEX_COLOR)), sizeof(c_int))
        except:
            pass


class ControlPanel(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, code_variable: ctk.Variable, time_variable: ctk.Variable):
        super().__init__(master=parent, fg_color=INPUT_BG_COLOR, corner_radius=0)
        self.pack(side=ctk.BOTTOM, fill=ctk.BOTH)
        # DATA.
        self.time = time_variable
        # COMPONENT.
        ctk.CTkEntry(master=self, textvariable=code_variable, text_color=TEXT_COLOR, fg_color=BG_COLOR,
                     border_color=TEXT_COLOR, border_width=1).pack(side=ctk.LEFT, padx=10, pady=10)
        self.buttons = [TextButton(self, option, time_variable)
                        for option in TIME_OPTIONS]
        # EVENT.
        self.time.trace('w', self.update_buttons)

    def update_buttons(self, *args):
        for button in self.buttons:
            color = TEXT_COLOR if button.cget(
                'text') != self.time.get() else HIGHLIGHT_COLOR
            button.configure(text_color=color)


class TextButton(ctk.CTkLabel):
    def __init__(self, parent: ctk.CTkFrame, title: str, link_variable: ctk.Variable):
        super().__init__(master=parent, text=title, text_color=TEXT_COLOR)
        self.pack(side=ctk.RIGHT, padx=10, pady=10)
        # EVENT.
        self.bind('<Button>', lambda event: link_variable.set(title))


class GraphPanel(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, data: DataFrame):
        super().__init__(master=parent, fg_color=BG_COLOR)
        self.pack(expand=True, fill=ctk.BOTH)
        # MATPLOTLIB.
        figure = Figure()
        # CHANGE THE SIZE OF FIGURE.
        figure.subplots_adjust(0, 0, 1, 1)
        # CHANGE THE BACKGROUND COLOR OF FIGURE.
        figure.patch.set_facecolor(BG_COLOR)
        # ADD A PLOT TO FIGURE.
        ax = figure.add_subplot()
        # CHANGE THE BACKGROUND COLOR OF PLOT.
        ax.set_facecolor(BG_COLOR)
        # HIDE THE BORDER OF PLOT.
        for side in ('left', 'right', 'top', 'bottom'):
            ax.spines[side].set_color(BG_COLOR)
        # ADJUST THE AXES OF PLOT.
        ax.tick_params(axis='x', direction='in', colors=TICK_COLOR, pad=-15)
        ax.yaxis.tick_right()
        ax.tick_params(axis='y', direction='in',
                       colors=HIGHLIGHT_COLOR, pad=-25)
        # CHANGE THE LINE COLOR.
        lines = ax.plot(data['Close'])
        lines[0].set_color(HIGHLIGHT_COLOR)
        # TKINTER.
        FigureCanvasTkAgg(figure=figure, master=self).get_tk_widget().pack(
            expand=True, fill=ctk.BOTH)


if __name__ == '__main__':
    Application().mainloop()
