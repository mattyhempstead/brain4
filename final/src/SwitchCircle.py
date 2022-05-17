from setting import *
from text import draw_text
from typing import Tuple
from ModeNode import ModeNode

class SwitchCircle:

    CIRCLE_HEIGHT = [240, 340, 440, 340]
    CIRCLE_WIDTH = [665, 465, 665, 865]

    def __init__(self):
        self.keys = ['Lowercase', 'Uppercase', 'Punctuation', 'Autocomplete']
        self.modes = []
        self.current_idx = -1
    
    def init_circle(self):
        for i in range(0, len(self.keys)):
            self.modes.append(ModeNode(SwitchCircle.CIRCLE_HEIGHT[i], SwitchCircle.CIRCLE_WIDTH[i]))
        self.set_keys(0)

        # for i in range(0, len(self.modes)):
        #     self.modes[i].set_left(self.modes[i-1])
        #     if i == len(self.modes) - 1:
        #         self.modes[i].set_right(self.modes[0])
        #     else:
        #         self.modes[i].set_right(self.modes[i+1])


    def get_current_mode(self):
        return self.modes[0]


    def set_keys(self, idx):
        for i in range(0, len(self.modes)):
            self.modes[i].set_key(self.keys[(i+idx)%4])
        self.current_idx = idx % 4
    

    def get_current_idx(self):
        return self.current_idx


    def render(self):
        for i in self.modes:
            i.render()
        self.render_edges()


    def render_edges(self):
        topleft = self.modes[0].rect.midleft
        topright = self.modes[0].rect.midright

        lefttop = self.modes[1].rect.midtop
        leftbottom = self.modes[1].rect.midbottom

        bottomleft = self.modes[2].rect.midleft
        bottomright = self.modes[2].rect.midright

        righttop = self.modes[3].rect.midtop
        rightbottom = self.modes[3].rect.midbottom

        pygame.draw.line(SCREEN, BLACK, topleft, lefttop)
        pygame.draw.line(SCREEN, BLACK, topright, righttop)
        pygame.draw.line(SCREEN, BLACK, leftbottom, bottomleft)
        pygame.draw.line(SCREEN, BLACK, rightbottom, bottomright)

        left_midpoint = (
            (topleft[0] + lefttop[0]) / 2,
            (topleft[1] + lefttop[1]) / 2,
        )
        self.render_edge_text("L", left_midpoint)

        right_midpoint = (
            (topright[0] + righttop[0]) / 2,
            (topright[1] + righttop[1]) / 2,
        )
        self.render_edge_text("R", right_midpoint)


    def render_edge_text(self, text:str, pos:Tuple[int,int]):
        # Circle background
        pygame.draw.circle(
            SCREEN, 
            ModeNode.EDGE_TEXT_CIRCLE_COLOR,
            pos, 
            ModeNode.EDGE_TEXT_CIRCLE_RADIUS
        )

        # Circle border
        pygame.draw.circle(
            SCREEN, 
            ModeNode.EDGE_TEXT_CIRCLE_BORDER_COLOR,
            pos, 
            ModeNode.EDGE_TEXT_CIRCLE_RADIUS,
            1
        )

        # Text
        draw_text(
            text = text,
            pos = pos,
            size = ModeNode.EDGE_TEXT_FONT_SIZE,
            color = DARK_GREY
        )

