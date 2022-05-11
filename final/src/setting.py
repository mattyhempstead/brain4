import matplotlib
matplotlib.use('Qt5agg')

import pygame, os, signal
from fast_autocomplete import AutoComplete

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_RETURN,
    KEYDOWN,
    QUIT,
)


GREY = (100, 100, 100)
DARK_GREY = (20, 20, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (211, 211, 211)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# NODE_LENGTH = 35

TREE_LAYER = 6
LAYER_HEIGHT = [150, 240, 330, 420, 510, [600, 650]]
LAYER_WIDTH = [[700],
               [500, 900],
               [340, 590, 790, 1060],
               [200, 350, 500, 625, 775, 900, 1050, 1200],
               [80, 160, 240, 320, 400, 480, 560, 640, 760, 840, 920, 1000, 1080, 1160, 1240, 1320],
               [20, 70, 115, 165, 205, 255, 295, 340, 380, 420, 465, 505, 550, 595, 640, 685, 715, 760, 805, 850, 895, 935, 980, 1020, 1060, 1105, 1145, 1195, 1235, 1285, 1330, 1380]]


# import words for autocomplete
WORDS = {}
""" 
words_10000.txt: https://www.mit.edu/~ecprice/wordlist.10000
words_10000_github.txt: https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt
"""
file = open("words_10000.txt", "r")
for word in file.read().split():
    WORDS[word] = {}
AUTOCOMPLETE = AutoComplete(words=WORDS)


# init the game
pygame.init()
pygame.display.set_caption("Virtual Keyboard")

# custom event
LEFT = pygame.USEREVENT + 1
RIGHT = pygame.USEREVENT + 2
SELECT = pygame.USEREVENT + 3

LEFT_EVENT = pygame.event.Event(LEFT)
RIGHT_EVENT = pygame.event.Event(RIGHT)
SELECT_EVENT = pygame.event.Event(SELECT)

""" 
----call the events----
 1. Convert event to Pygame's event datatype

LEFT_EVENT = pygame.event.Event(LEFT)
RIGHT_EVENT = pygame.event.Event(RIGHT)
SELECT_EVENT = pygame.event.Event(SELECT)

 2. post the events to the end of the queue

pygame.event.post(LEFT_EVENT)
pygame.event.post(RIGHT_EVENT)
pygame.event.post(SELECT_EVENT)
"""

# Set up the drawing window
WIDTH, HEIGHT = 1455, 800
RECT_X, RECT_Y = 35, 35
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])


FPS = 30  # None for unlimited


