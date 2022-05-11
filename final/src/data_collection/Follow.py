import pygame
import time
import numpy as np

from setting import *

from text import draw_text

class Follow:
    CIRCLE_RADIUS = 100
    CIRCLE_COLOR_BORDER = BLACK

    MOVE_TIMER = 3

    def __init__(self):
        
        self.x = WIDTH / 2
        self.y = HEIGHT / 2

        self.move_timer = time.time() + Follow.MOVE_TIMER


        self.action = None
        self.action_countdown = None


    @property
    def pos(self):
        return (self.x, self.y)

    def set_action(self, action:str):
        self.action = action

    def set_action_countdown(self, timer:float):
        self.action_countdown = timer

    def render(self):
        self.move()


        if self.action is None:
            pygame.draw.circle(
                SCREEN, 
                (0,255,0),
                self.pos, 
                Follow.CIRCLE_RADIUS,
            )

            draw_text(
                "GO",
                (self.x, self.y),
                80,
                color = (0,127,0)
            )
        else:
            pygame.draw.circle(
                SCREEN, 
                WHITE,
                self.pos, 
                Follow.CIRCLE_RADIUS,
            )

            draw_text(
                self.action,
                (self.x, self.y - 20),
                40,
                color = BLACK
            )

            draw_text(
                f"{self.action_countdown:4.2f}",
                (self.x, self.y + 20),
                50,
                color = BLACK
            )

        pygame.draw.circle(
            SCREEN, 
            Follow.CIRCLE_COLOR_BORDER,
            self.pos, 
            Follow.CIRCLE_RADIUS,
            2
        )

    def move(self):

        # Don't move while we are in a countdown?
        # if self.action is not None:
        #     return


        if time.time() < self.move_timer:
            return
        self.move_timer = time.time() + Follow.MOVE_TIMER*np.random.random()


        self.x = Follow.CIRCLE_RADIUS + (WIDTH - 2*Follow.CIRCLE_RADIUS) * np.random.random()
        self.y = Follow.CIRCLE_RADIUS + (HEIGHT - 2*Follow.CIRCLE_RADIUS) * np.random.random()



