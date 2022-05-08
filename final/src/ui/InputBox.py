import pygame

from colours import *

INPUT_WIDTH = 330
INPUT_HEIGHT = 50

INPUT_X = 595
INPUT_Y = 70

INPUT_BACKGROUND_COLOR = LIGHT_GREY
INPUT_FOREGROUND_COLOR = DARK_GREY


class InputBox:
    def __init__(self):
        self.user_input = ""

    def clear_text(self):
        self.user_input = ""

    def set_text(self, text:str):
        """ Sets entire user text """
        self.user_input = user_input

    def append_text(self, text:str):
        self.user_input += text

    def delete_text(self, num_chars:int = 1):
        self.user_input = self.user_input[:-num_chars]


    def render(self):
        input_bar = pygame.Rect((INPUT_WIDTH, INPUT_HEIGHT), (INPUT_X, INPUT_Y))
        pygame.draw.rect(SCREEN, INPUT_BACKGROUND_COLOR, input_bar)

        input_text = INPUT_FONT.render(self.user_input, True, INPUT_FOREGROUND_COLOR)
        SCREEN.blit(input_text, (INPUT_WIDTH, INPUT_HEIGHT + 10))
