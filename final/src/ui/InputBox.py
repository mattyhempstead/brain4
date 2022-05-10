import pygame

from setting import *

class InputBox:
    BORDER_COLOR = BLACK
    BACKGROUND_COLOR = WHITE

    FOREGROUND_COLOR = DARK_GREY

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

    def render(self):
        self.render_box()
        self.render_text()

    def render_box(self):
        input_bar = pygame.Rect((INPUT_WIDTH, INPUT_HEIGHT), (INPUT_X, INPUT_Y))
        pygame.draw.rect(SCREEN, InputBox.BACKGROUND_COLOR, input_bar)
        pygame.draw.rect(SCREEN, InputBox.BORDER_COLOR, input_bar, 1)

    def render_text(self):
        input_text = []
        for line in self.user_input:
            input_text.append(pygame.font.Font(None, 30).render(line, True, InputBox.FOREGROUND_COLOR))
        
        for i in range(0, len(input_text)):
            SCREEN.blit(input_text[i], (INPUT_WIDTH + 3, INPUT_HEIGHT + 2 + 20 * i + 2))
