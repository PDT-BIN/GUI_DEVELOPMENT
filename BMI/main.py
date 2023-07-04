import customtkinter as ctk
from settings import *


class Application(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=GREEN)
        # WINDOW SETUP.
        self.title('BMI Calculator')
        self.geometry('400x400')
        self.resizable(False, False)
        # LAYOUT.
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        # DATA STORAGE.
        self.data_type = ctk.BooleanVar(value=True)
        self.data_weight = ctk.DoubleVar(value=0)
        self.data_height = ctk.IntVar(value=100)
        self.data_BMI = ctk.StringVar()
        self.update_BMI()  # UPDATE FOR LOAD AT FIRST.
        # TRACE.
        self.data_height.trace('w', self.update_BMI)
        self.data_weight.trace('w', self.update_BMI)
        self.data_type.trace('w', self.change_units)
        # WIDGET.
        ResultText(self, self.data_BMI)
        self.weight_input = WeightInput(self, self.data_weight, self.data_type)
        self.height_input = HeightInput(self, self.data_height, self.data_type)
        UnitSwitcher(self, self.data_type)

    def update_BMI(self, *args):
        weight = self.data_weight.get()
        height = self.data_height.get() / 100
        self.data_BMI.set(round(weight / height ** 2, 2))

    def change_units(self, *args):
        self.weight_input.update_output()
        self.height_input.update_output(self.data_height.get())


class ResultText(ctk.CTkLabel):
    def __init__(self, parent, data_BMI):
        font = ctk.CTkFont(family=FONT, size=MAIN_FONT_SIZE, weight='bold')
        super().__init__(master=parent, text_color=WHITE, font=font, textvariable=data_BMI)
        self.grid(column=0, row=0, rowspan=2, sticky='news')


class WeightInput(ctk.CTkFrame):
    def __init__(self, parent, data_weight, data_type):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(column=0, row=2, sticky='news', padx=10, pady=10)
        self.data_weight = data_weight
        self.data_type = data_type
        # LAYOUT.
        self.rowconfigure(0, weight=1, uniform='b')
        self.columnconfigure(0, weight=2, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        self.columnconfigure(2, weight=3, uniform='b')
        self.columnconfigure(3, weight=1, uniform='b')
        self.columnconfigure(4, weight=2, uniform='b')
        # WIDGET.
        font = ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE, slant='italic')
        CTkButton = (lambda text, command: ctk.CTkButton(self, text=text, font=font, text_color=BLACK,
                                                         fg_color=LIGHT_GRAY, hover_color=GRAY,
                                                         corner_radius=BUTTON_RADIUS, command=command))
        # OUTPUT TEXT.
        self.data_output = ctk.StringVar()
        self.update_output()
        output = ctk.CTkLabel(
            self, font=font, text_color=BLACK, textvariable=self.data_output)
        output.grid(row=0, column=2)
        # BIG BUTTON.
        big_plus = CTkButton(
            '-', lambda: self.update_output(('minus', 'large')))
        big_plus.grid(row=0, column=0, sticky='ns', padx=8, pady=8)
        big_minus = CTkButton(
            '+', lambda: self.update_output(('plus', 'large')))
        big_minus.grid(row=0, column=4, sticky='ns', padx=8, pady=8)
        # SMALL BUTTON.
        small_plus = CTkButton(
            '+', lambda:  self.update_output(('plus', 'small')))
        small_plus.grid(row=0, column=3, padx=4, pady=4)
        small_minus = CTkButton(
            '-', lambda: self.update_output(('minus', 'small')))
        small_minus.grid(row=0, column=1, padx=4, pady=4)

    def update_output(self, data: tuple[str, str] = None):
        if data:
            # CONVERT DATA TYPE TO KILOGRAM UNIT.
            if self.data_type.get():
                amount = 1 if data[1] == 'large' else 0.1
            else:
                amount = 0.453592 if data[1] == 'large' else 0.453592 / 16
            # CALCULATE WEIGHT.
            if data[0] == 'plus':
                self.data_weight.set(self.data_weight.get() + amount)
            else:
                self.data_weight.set(max(0, self.data_weight.get() - amount))
        # DISPLAY WEIGHT INFORMATION.
        if self.data_type.get():
            self.data_output.set(f'{self.data_weight.get():.1f} kg')
        else:
            raw_ounches = self.data_weight.get() * 2.20462 * 16
            pounds, ounches = divmod(raw_ounches, 16)
            self.data_output.set(f'{pounds:.0f}lp {ounches:.0f}oz')


class HeightInput(ctk.CTkFrame):
    def __init__(self, parent, data_height, data_type):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(column=0, row=3, sticky='news', padx=10, pady=10)
        self.data_type = data_type
        # WIDGET.
        # HEIGHT SLIDER.
        slider = ctk.CTkSlider(self, button_color=GREEN, button_hover_color=GRAY, progress_color=GREEN,
                               fg_color=LIGHT_GRAY, variable=data_height, from_=100, to=250,
                               command=self.update_output)
        slider.pack(side='left', expand=True, fill='x', padx=10, pady=10)
        # OUTPUT TEXT.
        self.data_output = ctk.StringVar()
        self.update_output(data_height.get())
        output = ctk.CTkLabel(self, text_color=BLACK, textvariable=self.data_output, font=ctk.CTkFont(
            family=FONT, size=INPUT_FONT_SIZE, slant='italic'))
        output.pack(side='left', padx=20)

    def update_output(self, amount: int):
        # DISPLAY HEIGHT INFORMATION.
        if self.data_type.get():
            self.data_output.set(f'{amount / 100:.2f} m')
        else:
            feets, inches = divmod(amount / 2.54, 12)
            self.data_output.set(f'{feets:.0f}\'{inches:.0f}\"')


class UnitSwitcher(ctk.CTkLabel):
    def __init__(self, parent, data_type):
        font = ctk.CTkFont(family=FONT, size=SWITCH_FONT_SIZE, slant='italic')
        super().__init__(master=parent, text='Metric', text_color=DARK_GREEN, font=font)
        self.place(relx=0.98, rely=0.01, anchor='ne')
        self.data_type = data_type
        self.bind('<Button>', self.change_units)

    def change_units(self, event):
        self.data_type.set(not self.data_type.get())
        self.configure(text='Metric' if self.data_type.get() else 'Imperial')


if __name__ == '__main__':
    Application().mainloop()
