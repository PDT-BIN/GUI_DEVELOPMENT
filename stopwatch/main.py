from collections.abc import Callable
from math import cos, radians, sin
from time import time

import customtkinter as ctk
from settings import *


class Application(ctk.CTk):
    def __init__(self):
        # WINDOW SET-UP
        ctk.set_appearance_mode('DARK')
        super().__init__(fg_color=BLACK)
        self.geometry('300x600')
        self.iconbitmap('stopwatch/empty.ico')
        self.title('')
        self.resizable(False, False)
        # DATA.
        # LAYOUT.
        self.rowconfigure(0, weight=5, uniform='A')
        self.rowconfigure(1, weight=1, uniform='A')
        self.rowconfigure(2, weight=4, uniform='A')
        self.columnconfigure(0, weight=1, uniform='A')
        # FONTS.
        BUTTON_FONT = ctk.CTkFont(FONT, BUTTON_FONT_SIZE)
        # TIMER.
        self.timer = Timer()
        self.is_actived = False
        self.records: list[tuple[str, int, float]] = []
        # COMPONENT.
        self.clock = Clock(self)
        ControlButtons(self, BUTTON_FONT, self.start, self.pause,
                       self.resume, self.reset, self.lap)
        self.lap_container = LapContainer(self)

    def animate(self):
        if self.is_actived:
            self.clock.draw(self.timer.get_time())
            self.after(FRAMERATE, self.animate)

    def start(self):
        self.timer.start()
        self.is_actived = True
        self.animate()

    def pause(self):
        self.is_actived = False
        self.timer.pause()
        self.lap('PAUSE')

    def resume(self):
        self.timer.resume()
        self.is_actived = True
        self.animate()

    def reset(self):
        self.timer.reset()
        self.clock.draw()
        self.records.clear()
        self.lap_container.clear_container()

    def lap(self, type='LAP'):
        index = len([record for record in self.records if record[0]
                    == 'LAP']) + 1 if type == 'LAP' else ''
        self.records.append((type, index, self.timer.get_time()))
        self.lap_container.load_data(self.records)


class Timer:
    def __init__(self) -> None:
        self.start_time = None
        self.pause_time = None
        self.is_paused = False

    def start(self):
        self.start_time = time()

    def pause(self):
        self.pause_time = time()
        self.is_paused = True

    def resume(self):
        elapsed_time = time() - self.pause_time
        self.start_time += elapsed_time
        self.pause_time = None
        self.is_paused = False

    def reset(self):
        self.start_time = None
        self.pause_time = None
        self.is_paused = False

    def get_time(self):
        return int(round(time() - self.start_time, 2) * 1000)


class Clock(ctk.CTkCanvas):
    def __init__(self, parent: ctk.CTk):
        super().__init__(master=parent, background=BLACK,
                         bd=0, highlightthickness=0, relief=ctk.RIDGE)
        self.grid(row=0, column=0, sticky=ctk.NSEW, padx=5, pady=5)
        # START-UP.
        self.bind('<Configure>', self.load_data)

    def load_data(self, event):
        RADIUS = event.width / 2
        self.CENTER = RADIUS, RADIUS
        self.SIZE = event.width, event.height
        self.OUT_RADIUS = RADIUS * 0.95
        self.INN_RADIUS = RADIUS * 0.85
        self.MID_RADIUS = RADIUS * 0.9
        self.NUM_RADIUS = RADIUS * 0.7
        self.CEN_RADIUS = RADIUS * 0.2
        self.draw()

    def draw(self, milliseconds=0):
        # GET INFORMATION.
        seconds = milliseconds / 1000
        angle = (seconds % 60) * 6
        # DRAW.
        self.delete(ctk.ALL)
        self.draw_border()
        self.draw_time(milliseconds)
        self.draw_handle(angle)
        self.draw_center()

    def draw_center(self):
        self.create_oval(self.CENTER[0] - CENTER_GAP,
                         self.CENTER[1] - CENTER_GAP,
                         self.CENTER[0] + CENTER_GAP,
                         self.CENTER[1] + CENTER_GAP,
                         fill=BLACK, outline=ORANGE, width=LINE_WIDTH)

    def draw_handle(self, angle: float):
        sin_alpha = sin(radians(angle - 90))
        cos_alpha = cos(radians(angle - 90))
        # OUTER POINT.
        outer_x = self.CENTER[0] + self.OUT_RADIUS * cos_alpha
        outer_y = self.CENTER[1] + self.OUT_RADIUS * sin_alpha
        # START POINT.
        start_x = self.CENTER[0] - self.CEN_RADIUS * cos_alpha
        start_y = self.CENTER[1] - self.CEN_RADIUS * sin_alpha
        self.create_line((start_x, start_y), (outer_x, outer_y),
                         fill=ORANGE, width=LINE_WIDTH)

    def draw_border(self):
        for angle in range(360):
            sin_alpha = sin(radians(angle - 90))
            cos_alpha = cos(radians(angle - 90))
            # OUTER POINT.
            outer_x = self.CENTER[0] + self.OUT_RADIUS * cos_alpha
            outer_y = self.CENTER[1] + self.OUT_RADIUS * sin_alpha
            if angle % 30 == 0:
                # DRAW MARK.
                inner_x = self.CENTER[0] + self.INN_RADIUS * cos_alpha
                inner_y = self.CENTER[1] + self.INN_RADIUS * sin_alpha
                self.create_line((outer_x, outer_y), (inner_x, inner_y),
                                 fill=WHITE, width=LINE_WIDTH)
                # DRAW NUMBER.
                number_x = self.CENTER[0] + self.NUM_RADIUS * cos_alpha
                number_y = self.CENTER[1] + self.NUM_RADIUS * sin_alpha
                self.create_text((number_x, number_y), text=f'{angle // 6}',
                                 font=f'{FONT} {CLOCK_FONT_SIZE}', fill=WHITE)
            elif angle % 6 == 0:
                middle_x = self.CENTER[0] + self.MID_RADIUS * cos_alpha
                middle_y = self.CENTER[1] + self.MID_RADIUS * sin_alpha
                self.create_line((outer_x, outer_y), (middle_x, middle_y),
                                 fill=GREY, width=LINE_WIDTH)

    def draw_time(self, milliseconds: int):
        self.create_text((self.CENTER[0], self.CENTER[1] + 50), anchor=ctk.CENTER, fill=WHITE,
                         text=Clock.strftime(milliseconds), font=f'{FONT} {TIME_FONT_SIZE} bold')

    @staticmethod
    def strftime(milliseconds: int) -> str:
        # SPLIT INFORMATION.
        seconds, remainders = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        # FORMAT TIME.
        seconds = f'{seconds:02} . {remainders // 10:02}'
        minutes = f'{minutes:02} : ' if minutes > 0 else ''
        hours = f'{hours:02} : ' if hours > 0 else ''
        # RETURN TEXT.
        return hours + minutes + seconds


class ControlButtons(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, font: ctk.CTkFont, start: Callable, pause: Callable,
                 resume: Callable, reset: Callable, lap: Callable):
        super().__init__(master=parent, fg_color='transparent', corner_radius=0)
        self.grid(row=1, column=0, sticky=ctk.NSEW, padx=5, pady=5)
        # INTERACTIVE METHOD.
        self.start = start
        self.pause = pause
        self.resume = resume
        self.reset = reset
        self.lap = lap
        self.state = 'OFF'
        # LAYOUT.
        self.rowconfigure(0, weight=1, uniform='B')
        self.columnconfigure(0, weight=1, uniform='B')
        self.columnconfigure(1, weight=9, uniform='B')
        self.columnconfigure(2, weight=1, uniform='B')
        self.columnconfigure(3, weight=9, uniform='B')
        self.columnconfigure(4, weight=1, uniform='B')
        # COMPONENT.
        self.lap_button = ctk.CTkButton(master=self, font=font, fg_color=GREY, text='LAP',
                                        state=ctk.DISABLED, command=self.handle_lap)
        self.run_button = ctk.CTkButton(master=self, font=font, fg_color=GREEN, text='START',
                                        text_color=GREEN_TEXT, hover_color=GREEN_HIGHLIGHT,
                                        command=self.handle_run)
        # PLACE.
        self.lap_button.grid(row=0, column=1, sticky=ctk.NSEW)
        self.run_button.grid(row=0, column=3, sticky=ctk.NSEW)

    def handle_run(self):
        # CHANGE STATE.
        match self.state:
            case 'OFF':
                self.start()
                self.state = 'ON'
            case 'ON':
                self.pause()
                self.state = 'PAUSE'
            case 'PAUSE':
                self.resume()
                self.state = 'ON'
        # CHANGE BUTTON.
        self.update_buttons()

    def handle_lap(self):
        # CHANGE STATE.
        if self.state == 'ON':
            self.lap()
        else:
            self.reset()
            self.state = 'OFF'
        # CHANGE BUTTON.
        self.update_buttons()

    def update_buttons(self):
        match self.state:
            case 'OFF':
                self.lap_button.configure(
                    state=ctk.DISABLED, text='LAP', fg_color=GREY)
            case 'ON':
                self.run_button.configure(text='STOP', text_color=RED_TEXT,
                                          fg_color=RED, hover_color=RED_HIGHLIGHT)
                self.lap_button.configure(state=ctk.NORMAL, text='LAP', text_color=ORANGE_DARK_TEXT,
                                          fg_color=ORANGE_DARK, hover_color=ORANGE_HIGHLIGHT)
            case 'PAUSE':
                self.run_button.configure(text='START', text_color=GREEN_TEXT,
                                          fg_color=GREEN, hover_color=GREEN_HIGHLIGHT)
                self.lap_button.configure(text='RESET')


class LapContainer(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk):
        super().__init__(master=parent, fg_color=BLACK)
        self.grid(row=2, column=0, sticky=ctk.NSEW, padx=5, pady=5)
        # COMPONENT.
        self.canvas: ctk.CTkCanvas = None

    def clear_container(self):
        if self.canvas:
            self.canvas.pack_forget()

    def load_data(self, data: list[tuple[str, int, float]]):
        self.clear_container()
        # SET-UP.
        data_length = len(data)
        list_height = data_length * LAP_ITEM_HEIGHT
        is_scrollable = list_height > self.winfo_height()
        scroll_height = max(list_height, self.winfo_height())
        # CREATE CANVAS.
        self.canvas = ctk.CTkCanvas(master=self, background=BLACK, bd=0, highlightthickness=0, relief=ctk.RIDGE,
                                    scrollregion=(0, 0, self.winfo_width(), scroll_height))
        self.canvas.pack(expand=True, fill=ctk.BOTH)
        # LOAD DATA.
        display_frame = ctk.CTkFrame(master=self, fg_color=BLACK)
        DATA_FONT = ctk.CTkFont(FONT, 14, 'bold')
        for index, record in enumerate(data):
            self.initialize_item(
                display_frame, record, index == data_length - 1, DATA_FONT)
        # SCROLL BAR.
        if is_scrollable:
            self.canvas.bind_all(
                '<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), 'units'))
        # DRAW DATA.
        self.canvas.create_window((0, 0), anchor=ctk.NW, window=display_frame,
                                  width=self.winfo_width(), height=list_height)

    def initialize_item(self, parent: ctk.CTkFrame, data: tuple[str, int, float], is_final: bool,
                        font: ctk.CTkFont):
        item = ctk.CTkFrame(master=parent, fg_color=BLACK)
        data_frame = ctk.CTkFrame(master=item, fg_color=BLACK)
        # DISPLAY DATA.
        ctk.CTkLabel(master=data_frame, text=f'{data[0]} {data[1]}', font=font).pack(
            side=ctk.LEFT, padx=10)
        ctk.CTkLabel(master=data_frame, text=f'{Clock.strftime(data[2])}', font=font).pack(
            side=ctk.RIGHT, padx=10)
        # DISPLAY LINE.
        if not is_final:
            ctk.CTkFrame(master=item, fg_color=GREY, height=2).pack(
                side=ctk.BOTTOM, fill=ctk.X)
        data_frame.pack(expand=True, fill=ctk.BOTH, pady=3)
        item.pack(fill=ctk.X)


if __name__ == '__main__':
    Application().mainloop()
