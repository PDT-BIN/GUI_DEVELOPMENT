from collections.abc import Callable

import customtkinter as ctk
from panel import (DropDownPanel, ResetButton, SaveButton, SaveFilePanel,
                   SavePathPanel, SegmentPanel, SliderPanel, SwitchPanel)
from settings import *


class Menu(ctk.CTkTabview):
    def __init__(self, parent, binding_source: dict[str, dict[str, ctk.Variable]],
                 save_image: Callable[[str, str, str], None]):
        super().__init__(master=parent)
        self.grid(column=0, row=0, sticky=ctk.NSEW, padx=10, pady=10)
        # TABS.
        self.add('POSITION')
        self.add('COLOUR')
        self.add('EFFECT')
        self.add('EXPORT')
        # FRAMES.
        PositionFrame(self.tab('POSITION'), binding_source['POSITION'])
        ColourFrame(self.tab('COLOUR'), binding_source['COLOUR'])
        EffectFrame(self.tab('EFFECT'), binding_source['EFFECT'])
        ExportFrame(self.tab('EXPORT'), save_image)


class PositionFrame(ctk.CTkFrame):
    def __init__(self, parent, data_source: dict[str, ctk.Variable]):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill=ctk.BOTH)
        # WIDGET.
        SliderPanel(self, 'Rotation', data_source['ROTATE'], 0, 360)
        SliderPanel(self, 'Zoom', data_source['ZOOM'], 0, 200)
        SegmentPanel(self, 'Flip', data_source['FLIP'], FLIP_OPTIONS)
        # RESET BUTTON.
        ResetButton(self, (data_source['ROTATE'], DEFAULT_ROTATE),
                    (data_source['ZOOM'], DEFAULT_ZOOM), (data_source['FLIP'], FLIP_OPTIONS[0]))


class ColourFrame(ctk.CTkFrame):
    def __init__(self, parent, data_source: dict[str, ctk.Variable]):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill=ctk.BOTH)
        # WIDGET.
        SwitchPanel(
            self, ('B/W', data_source['GRAYSCALE']), ('Invert', data_source['INVERT']))
        SliderPanel(self, 'Brightness', data_source['BRIGHTNESS'], 0, 5)
        SliderPanel(self, 'Vibrance', data_source['VIBRANCE'], 0, 5)
        # RESET BUTTON.
        ResetButton(self, (data_source['GRAYSCALE'], DEFAULT_GRAYSCALE), (data_source['INVERT'], DEFAULT_INVERT),
                    (data_source['BRIGHTNESS'], DEFAULT_BRIGHTNESS), (data_source['VIBRANCE'], DEFAULT_VIBRANCE))


class EffectFrame(ctk.CTkFrame):
    def __init__(self, parent, data_source: dict[str, ctk.Variable]):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill=ctk.BOTH)
        # WIDGET.
        DropDownPanel(self, data_source['EFFECT'], EFFECT_OPTIONS)
        SliderPanel(self, 'Blur', data_source['BLUR'], 0, 10)
        SliderPanel(self, 'Contrast', data_source['CONTRAST'], 0, 10)
        # RESET BUTTON.
        ResetButton(self, (data_source['EFFECT'], EFFECT_OPTIONS[0]),
                    (data_source['BLUR'], DEFAULT_BLUR), (data_source['CONTRAST'], DEFUALT_CONTRAST))


class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent, save_image: Callable[[str, str, str], None]):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill=ctk.BOTH)
        # BINDING DATA.
        self.bds_file_name = ctk.StringVar()
        self.bds_extension = ctk.StringVar(value='png')
        self.bds_file_path = ctk.StringVar()
        # WIDGET.
        SaveFilePanel(self, self.bds_file_name, self.bds_extension)
        SavePathPanel(self, self.bds_file_path)
        SaveButton(self, self.bds_file_name, self.bds_extension,
                   self.bds_file_path, save_image)
