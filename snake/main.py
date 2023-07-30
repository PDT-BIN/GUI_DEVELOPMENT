from random import randint
from sys import exit

import customtkinter as ctk
from settings import *


class Game(ctk.CTk):
    def __init__(self):
        # WINDOW SET-UP.
        super().__init__(fg_color='BLACK')
        self.geometry(f'{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}')
        self.iconbitmap('snake/empty.ico')
        self.title('')
        # LAYOUT.
        self.columnconfigure(tuple(range(FIELDS[0])), weight=1, uniform='A')
        self.rowconfigure(tuple(range(FIELDS[1])), weight=1, uniform='A')
        # FRAME CONTAINER.
        self.container: list[tuple[ctk.CTkFrame, tuple]] = []
        # SNAKE.
        self.snake = [(START_POSITION[0] - index, START_POSITION[1])
                      for index in range(3)]
        self.direction = DIRECTIONS['RIGHT']
        self.bind('<Key>', self.input)
        # APPLE.
        self.place_apple()
        # RUN GAME.
        self.animate()

    def animate(self):
        # SNAKE UPDATE.
        NEW_HEAD = (self.snake[0][0] + self.direction[0],
                    self.snake[0][1] + self.direction[1])
        self.snake.insert(0, NEW_HEAD)
        if NEW_HEAD == self.apple:
            # APPLE UPDATE.
            self.place_apple()
        else:
            self.snake.pop()
        # CHECK.
        self.check_game_over()
        # REDRAW.
        self.draw()
        # LOOP.
        self.after(250, self.animate)

    def check_game_over(self):
        SNAKE_HEAD = self.snake[0]
        if (not (LEFT_LIMIT <= SNAKE_HEAD[0] < RIGHT_LIMIT and TOP_LIMIT <= SNAKE_HEAD[1] < BOTTOM_LIMIT)
                or SNAKE_HEAD in self.snake[1:]):
            self.destroy()
            exit()

    def input(self, event):
        match event.keycode:
            case 37:
                if self.direction != DIRECTIONS['RIGHT']:
                    self.direction = DIRECTIONS['LEFT']
            case 38:
                if self.direction != DIRECTIONS['DOWN']:
                    self.direction = DIRECTIONS['UP']
            case 39:
                if self.direction != DIRECTIONS['LEFT']:
                    self.direction = DIRECTIONS['RIGHT']
            case 40:
                if self.direction != DIRECTIONS['UP']:
                    self.direction = DIRECTIONS['DOWN']

    def place_apple(self):
        self.apple = randint(0, FIELDS[0] - 1), randint(0, FIELDS[1] - 1)

    def draw(self):
        # EMPTY CONTAINER.
        for frame, _ in self.container:
            frame.grid_forget()
        self.container.clear()
        # LOAD TO CONTAINER.
        self.container.append(
            (ctk.CTkFrame(master=self, fg_color=APPLE_COLOR), self.apple))
        for index, position in enumerate(self.snake):
            color = SNAKE_BODY_COLOR if index != 0 else SNAKE_HEAD_COLOR
            self.container.append(
                (ctk.CTkFrame(master=self, fg_color=color, corner_radius=0), position))
        # DRAW.
        for frame, position in self.container:
            frame.grid(column=position[0], row=position[1])


if __name__ == '__main__':
    Game().mainloop()
