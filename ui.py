# Import and initialize the pygame library
import pygame
import Keys
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_RETURN,
    KEYDOWN,
    QUIT,
)

# custom event
LEFT = pygame.USEREVENT + 1
RIGHT = pygame.USEREVENT + 2
SELECT = pygame.USEREVENT + 3

""" 
----call the events----
 1. Convert event to Pygame's event type
 
LEFT_EVENT = pygame.event.Event(LEFT)
RIGHT_EVENT = pygame.event.Event(RIGHT)
SELECT_EVENT = pygame.event.Event(SELECT)

 2. post the events to the end of the queue
 
pygame.event.post(LEFT_EVENT)
pygame.event.post(RIGHT_EVENT)
pygame.event.post(SELECT_EVENT)
"""



pygame.init()
pygame.display.set_caption("Virtual Keyboard")

# Set up the drawing window
WIDTH, HEIGHT = 1255, 800
RECT_X, RECT_Y = 55, 40
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])

GREY = (100, 100, 100)
DARK_GREY = (20, 20, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (211, 211, 211)

KEY_FONT = pygame.font.Font(None, 45)
OPTION_FONT = pygame.font.Font(None, 25)
INPUT_FONT = pygame.font.Font(None, 65)

NUM_LAYER = 5
LAYER_HEIGHT = [230, 340, 468, 594, 710]
LAYER_WIDTH = [[600], [445, 755], [330, 485, 715, 870], [230, 330, 430, 535, 665, 770, 870, 970], [140, 200, 265, 325, 390, 450, 510, 570, 630, 690, 750, 810, 875, 935, 1000, 1060]]

KEYS = Keys.Keys()
KEYS.init_trees()
KEYS.root.height = LAYER_HEIGHT[0]
KEYS.root.width = LAYER_WIDTH[0][0]

INPUT_WIDTH = 330
INPUT_HEIGHT = 100

user_input = ""
running = True
alpha = True
upper = False
cursor = KEYS.root

while running:

    # event handler
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # move the cursor
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                if cursor.is_leaf():
                    cursor = KEYS.root
                else:
                    cursor = cursor.left

            if event.key == K_RIGHT:
                if cursor.is_leaf():
                    cursor = KEYS.root
                else:
                    cursor = cursor.right

            if event.key == K_RETURN:
                key = ""
                if alpha:
                    key = cursor.alpha_key
                else:
                    key = cursor.punc_key

                if len(key) == 1:
                    if not upper and key.isalpha():
                        user_input += key.lower()
                    else:
                        user_input += key
                elif key == "Space":
                    user_input += " "
                elif key == "Delete":
                    user_input = user_input[:-1]
                elif key == "Clear":
                    user_input = ""
                elif key == "U/L":
                    upper = not upper
                elif key == "123":
                    cursor = KEYS.root
                    alpha = False
                elif key == "abc":
                    upper = False
                    cursor = KEYS.root
                    alpha = True


    # fill the background with white
    SCREEN.fill(WHITE)

    # draw the input
    input_bar = pygame.Rect((INPUT_WIDTH, INPUT_HEIGHT), (595, 70))
    pygame.draw.rect(SCREEN, LIGHT_GREY, input_bar)
    input = INPUT_FONT.render(user_input, True, DARK_GREY)
    SCREEN.blit(input, (INPUT_WIDTH, INPUT_HEIGHT + 10))

    # BFS thru the nodes and draw the rectangles with the alpha key
    fringe = [KEYS.root]
    i = j = 0  # i-height, j-width
    while len(fringe) > 0:
        tmp = fringe.pop(0)

        tmp.width = LAYER_WIDTH[i][j]
        tmp.height = LAYER_HEIGHT[i]

        tmp.rect = pygame.Rect((tmp.width, tmp.height), (RECT_X, RECT_Y))
        if not tmp.is_leaf():
            fringe.append(tmp.left)
            fringe.append(tmp.right)

        # draw the rectangle
        pygame.draw.rect(SCREEN, BLACK, tmp.rect, 1)

        # draw the lines connecting to the children
        if not tmp.is_root():
            start_pos = (tmp.width + 27.5, tmp.height)
            end_pos = (tmp.parent.width + 27.5, tmp.parent.height + 40)

            pygame.draw.line(SCREEN, BLACK, start_pos, end_pos)

        # create surface for keys
        rect_surf = pygame.Surface((RECT_X-2, RECT_Y-2))
        if cursor.width == tmp.width and cursor.height == tmp.height:
            rect_surf.fill(LIGHT_GREY)
        else:
            rect_surf.fill(WHITE)

        # option or key
        if alpha:
            key = tmp.alpha_key
            if len(tmp.alpha_key) > 1:
                if key == "U/L":
                    if upper:
                        key = "Lower"
                    else:
                        key = "Upper"
                surface = OPTION_FONT.render(key, True, DARK_GREY)

                if len(key) == 5:
                    rect_surf.blit(surface, (1, 8))
                elif len(key) == 3:
                    rect_surf.blit(surface, (8, 8))
                else:
                    rect_surf.blit(surface, (0, 8))

                SCREEN.blit(rect_surf, (tmp.width + 1, tmp.height + 1))
            else:
                if not upper:
                    key = key.lower()

                surface = KEY_FONT.render(key, True, DARK_GREY)
                rect_surf.blit(surface, (16, 4))
                SCREEN.blit(rect_surf, (tmp.width + 1, tmp.height + 1))
        else:
            if len(str(tmp.punc_key)) > 1:
                surface = OPTION_FONT.render(tmp.punc_key, True, DARK_GREY)

                if len(tmp.punc_key) == 5:
                    rect_surf.blit(surface, (1, 8))
                elif len(tmp.punc_key) == 3:
                    rect_surf.blit(surface, (8, 8))
                else:
                    rect_surf.blit(surface, (0, 8))

                SCREEN.blit(rect_surf, (tmp.width + 1, tmp.height + 1))
            else:
                surface = KEY_FONT.render(str(tmp.punc_key), True, DARK_GREY)
                rect_surf.blit(surface, (15, 4))
                SCREEN.blit(rect_surf, (tmp.width + 1, tmp.height + 1))

        j += 1
        if j >= len(LAYER_WIDTH[i]):
            i += 1
            j = 0

    # Flip the display
    pygame.display.flip()


# Done! Time to quit.
pygame.quit()