import customtkinter as ctk
import darkdetect
from buttons import (Button, ImageButton, MathButton, MathImageButton,
                     NumberButton)
from PIL import Image
from settings import *


class Application(ctk.CTk):
    def __init__(self, dark_mode: bool):
        super().__init__(fg_color=(WHITE, BLACK))
        # SET APPERANCE.
        self.title('Calculator')
        self.iconbitmap('calculator/image/icon.ico')
        ctk.set_appearance_mode('DARK' if dark_mode else 'LIGHT')
        self.center_window()
        self.resizable(False, False)
        # LAYOUT.
        self.rowconfigure(tuple(range(MAIN_ROWS)), weight=1, uniform='A')
        self.columnconfigure(tuple(range(MAIN_COLS)), weight=1, uniform='A')
        # DATA BINDING.
        self.str_result = ctk.StringVar(value='0')
        self.str_formula = ctk.StringVar()
        self.current_number = []
        self.full_operation = []
        # WIDGET.
        self.load_data()

    def center_window(self):
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}' +
                      f'+{(self.winfo_screenwidth() - APP_SIZE[0]) // 2}' +
                      f'+{(self.winfo_screenheight() - APP_SIZE[1]) // 2}')

    def load_data(self):
        # FONT.
        MAIN_FONT = ctk.CTkFont(FONT, NORMAL_FONT_SIZE)
        RESULT_FONT = ctk.CTkFont(FONT, OUTPUT_FONT_SIZE)
        # OUTPUT.
        OutputText(self, 0, 'SE', MAIN_FONT, self.str_formula)
        OutputText(self, 1, 'E', RESULT_FONT, self.str_result)
        # CLEAR BUTTON.
        Button(self, OPERATORS['clear']['text'], OPERATORS['clear']['col'],
               OPERATORS['clear']['row'], MAIN_FONT, self.clear)
        # PERCENT BUTTON.
        Button(self, OPERATORS['percent']['text'], OPERATORS['percent']['col'],
               OPERATORS['percent']['row'], MAIN_FONT, self.percent)
        # INVERT BUTTON.
        INVERT_IMAGES = ctk.CTkImage(Image.open(OPERATORS['invert']['image']['dark']),
                                     Image.open(OPERATORS['invert']['image']['light']))
        ImageButton(self, OPERATORS['invert']['text'], OPERATORS['invert']['col'],
                    OPERATORS['invert']['row'], INVERT_IMAGES, self.invert)
        # NUMBER BUTTONS.
        for key, value in NUM_POSITIONS.items():
            NumberButton(self, str(key), value['col'], value['row'],
                         MAIN_FONT, value['span'], self.press_numb)
        # MATH BUTTONS.
        for key, value in MATH_POSITIONS.items():
            if not value['image']:
                MathButton(self, value['character'], key,
                           value['col'], value['row'], MAIN_FONT, self.press_math)
            else:
                DIVISION_IMAGES = ctk.CTkImage(Image.open(value['image']['dark']),
                                               Image.open(value['image']['light']))
                MathImageButton(self, value['character'], key, value['col'],
                                value['row'], DIVISION_IMAGES, self.press_math)

    def press_numb(self, value: str):
        self.current_number.append(value)
        self.str_result.set(''.join(self.current_number))

    def press_math(self, value: str):
        if number := ''.join(self.current_number):
            self.full_operation.append(number)
            if value != '=':
                self.full_operation.append(value)
                self.current_number.clear()
                self.str_formula.set(' '.join(self.full_operation))
                self.str_result.set('')
            else:
                # CALCULATE.
                formula = ' '.join(self.full_operation)
                result = eval(formula)
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 3)
                # DISPLAY.
                self.str_formula.set(formula)
                self.str_result.set(result)
                # NEW OPERATION.
                self.full_operation.clear()
                self.current_number = [str(result)]

    def clear(self):
        self.str_result.set('0')
        self.str_formula.set('')
        self.current_number.clear()
        self.full_operation.clear()

    def percent(self):
        if number := ''.join(self.current_number):
            number = float(number) / 100
            self.current_number = list(str(number))
            self.str_result.set(''.join(self.current_number))

    def invert(self):
        if number := ''.join(self.current_number):
            if float(number) > 0:
                self.current_number.insert(0, '-')
            else:
                self.current_number.remove('-')
            self.str_result.set(''.join(self.current_number))


class OutputText(ctk.CTkLabel):
    def __init__(self, parent, row_index: int, anchor: str, font: ctk.CTkFont, data_binding: ctk.Variable):
        super().__init__(master=parent, font=font, textvariable=data_binding)
        self.grid(column=0, row=row_index,
                  columnspan=4, sticky=anchor, padx=10)


if __name__ == '__main__':
    Application(darkdetect.isDark()).mainloop()
