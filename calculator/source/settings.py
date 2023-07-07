# SIZE.
APP_SIZE = 400, 700
MAIN_ROWS = 7
MAIN_COLS = 4

# TEXT.
FONT = 'Helvetica'
OUTPUT_FONT_SIZE = 64
NORMAL_FONT_SIZE = 32

STYLE = {'gap': 0.5, 'corner-radius': 0}

NUM_POSITIONS = {
    '.': {'col': 2, 'row': 6, 'span': 1},
    0: {'col': 0, 'row': 6, 'span': 2},
    1: {'col': 0, 'row': 5, 'span': 1},
    2: {'col': 1, 'row': 5, 'span': 1},
    3: {'col': 2, 'row': 5, 'span': 1},
    4: {'col': 0, 'row': 4, 'span': 1},
    5: {'col': 1, 'row': 4, 'span': 1},
    6: {'col': 2, 'row': 4, 'span': 1},
    7: {'col': 0, 'row': 3, 'span': 1},
    8: {'col': 1, 'row': 3, 'span': 1},
    9: {'col': 2, 'row': 3, 'span': 1},
}

MATH_POSITIONS = {
    '/': {'col': 3, 'row': 2, 'character': '', 'image':
          {'light': 'calculator/image/divide_light.png', 'dark': 'calculator/image/divide_dark.png'}},
    '*': {'col': 3, 'row': 3, 'character': 'x', 'image': None},
    '-': {'col': 3, 'row': 4, 'character': '-', 'image': None},
    '+': {'col': 3, 'row': 5, 'character': '+', 'image': None},
    '=': {'col': 3, 'row': 6, 'character': '=', 'image': None},
}

OPERATORS = {
    'clear': {'col': 0, 'row': 2, 'text': 'AC', 'image': None},
    'invert': {'col': 1, 'row': 2, 'text': '', 'image':
               {'light': 'calculator/image/invert_light.png', 'dark': 'calculator/image/invert_dark.png'}},
    'percent': {'col': 2, 'row': 2, 'text': '%', 'image': None}
}

# COLOR.
COLORS = {
    'light-gray': {'fg': ('#505050', '#D4D4D2'), 'hover': ('#686868', '#EFEFED'), 'text': ('WHITE', 'BLACK')},
    'dark-gray': {'fg': ('#D4D4D2', '#505050'), 'hover': ('#EFEFED', '#686868'), 'text': ('BLACK', 'WHITE')},
    'orange': {'fg': '#FF9500', 'hover': '#FFB143', 'text': ('BLACK', 'WHITE')},
    'orange-hightlight': {'fg': 'WHITE', 'hover': 'WHITE', 'text': ('BLACK', '#FF9500')}
}

BLACK = '#000000'
WHITE = '#EEEEEE'
