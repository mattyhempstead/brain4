import pygame
import time
from text import draw_text

from setting import *

class InputBox:
    BORDER_COLOR = BLACK
    BACKGROUND_COLOR = WHITE

    FOREGROUND_COLOR = DARK_GREY

    CURSOR_BLINK_TIME = 0.5
    CURSOR_COLOR = DARK_GREY

    LINE_HEIGHT = 22

    X_POS = 800
    Y_POS = 100
    WIDTH = 300
    HEIGHT = 30

    def __init__(self):
        self.user_input = [""]

        self.cursor_visible = False
        self.cursor_blink_timer = 0


    def clear_text(self):
        self.user_input = [""]

    def set_text(self, text:str):
        """ Sets entire user text """
        self.user_input[-1] = text

    def get_user_input(self):
        return self.user_input

    def append_text(self, text:str):
        self.user_input[len(self.user_input)-1] += text

    def delete_text(self, num_chars:int = 1):
        if len(self.user_input[len(self.user_input)-1]) == 0:
            if len(self.user_input) != 1:
                self.user_input.pop(len(self.user_input)-1)
        else:
            self.user_input[len(self.user_input)-1] = self.user_input[len(self.user_input)-1][:-num_chars]

    def new_line(self):
        self.user_input.append("")

    def render(self):
        self.render_box()
        self.render_text()

    def render_box(self):
        input_bar = pygame.Rect((InputBox.WIDTH, InputBox.HEIGHT), (InputBox.X_POS, InputBox.Y_POS))
        pygame.draw.rect(SCREEN, InputBox.BACKGROUND_COLOR, input_bar)
        pygame.draw.rect(SCREEN, InputBox.BORDER_COLOR, input_bar, 1)

    def render_text(self):
        input_text = []
        for line in self.user_input:
            input_text.append(pygame.font.Font(None, 30).render(line, True, InputBox.FOREGROUND_COLOR))
        
        for i in range(0, len(input_text)):
            rect_pos = (
                InputBox.WIDTH + 3, 
                InputBox.HEIGHT + 2 + InputBox.LINE_HEIGHT * i + 2
            )
            SCREEN.blit(input_text[i], rect_pos)

            if i == len(input_text) - 1:
                self.render_cursor(input_text[i].get_rect(), rect_pos)

    def render_cursor(self, rect_text, rect_pos):
        if time.time() >= self.cursor_blink_timer:
            # Toggle cursor and reset time
            self.cursor_blink_timer = time.time() + InputBox.CURSOR_BLINK_TIME
            self.cursor_visible = not self.cursor_visible

        if not self.cursor_visible:
            return

        rect_text.topleft = rect_pos

        cursor_top = rect_text.topright
        cursor_top = (cursor_top[0] + 2, cursor_top[1])

        cursor_bottom = rect_text.bottomright
        cursor_bottom = (cursor_bottom[0] + 2, cursor_bottom[1] - 4)

        pygame.draw.line(SCREEN, InputBox.CURSOR_COLOR, cursor_top, cursor_bottom, 2)

