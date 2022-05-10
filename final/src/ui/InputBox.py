import pygame

from setting import *

INPUT_BACKGROUND_COLOR = LIGHT_GREY
INPUT_FOREGROUND_COLOR = DARK_GREY


class InputBox:
    def __init__(self):
        self.user_input = [""]

    def clear_text(self):
        self.user_input = [""]

    def set_text(self, text:str):
        """ Sets entire user text """
        self.user_input = text

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

    def render(self, SCREEN, p):
        input_bar = p.Rect((INPUT_WIDTH, INPUT_HEIGHT), (INPUT_X, INPUT_Y))
        pygame.draw.rect(SCREEN, INPUT_BACKGROUND_COLOR, input_bar)

        input_text = []
        for line in self.user_input:
            input_text.append(p.font.Font(None, 30).render(line, True, INPUT_FOREGROUND_COLOR))
        
        for i in range(0, len(input_text)):
            SCREEN.blit(input_text[i], (INPUT_WIDTH, INPUT_HEIGHT + 2 + 20 * i))
