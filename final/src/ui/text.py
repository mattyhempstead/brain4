from functools import cache
from typing import Tuple
import pygame

from setting import *



@cache
def get_font(size:int):
    """ A cached function to return fonts """
    return pygame.font.Font(None, size)


def draw_text(text:str, pos:Tuple[int,int], size:int, color=BLACK, center=True):
    """
    Draws text on screen.

    Example
    text: "apple"
    pos: (200,300)
    size: 25
    color: (0,0,255)
    center: True
    """
    font = get_font(size)
    text = font.render(text, True, color)

    # centre text
    # TODO: Add other alignment options
    text_rect = text.get_rect()
    if center:
        text_rect.center = pos

    SCREEN.blit(text, text_rect)

