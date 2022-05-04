# Import and initialize the pygame library
import pygame, os, signal
import Keys
from fast_autocomplete import AutoComplete

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_RETURN,
    KEYDOWN,
    QUIT,
)

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
AUTOCOMPLETE_FONT = pygame.font.Font(None, 18)

NUM_LAYER = 6
LAYER_HEIGHT = [160, 260, 380, 500, 615, 730]
LAYER_WIDTH = [[600],
               [445, 755],
               [330, 485, 715, 870],
               [230, 330, 430, 535, 665, 770, 870, 970],
               [140, 200, 265, 325, 390, 450, 510, 570, 630, 690, 750, 810, 875, 935, 1000, 1060],
               [140, 200, 265, 325, 390, 450, 510, 570, 630, 690, 750, 810, 875, 935, 1000, 1060]]

KEYS = Keys.Keys()
KEYS.init_trees()
KEYS.root.height = LAYER_HEIGHT[0]
KEYS.root.width = LAYER_WIDTH[0][0]

INPUT_WIDTH = 330
INPUT_HEIGHT = 50

def signal_handler(signum, stack):
    print("sighandler " + str(signum))
    if signum == 30:
        pygame.event.post(LEFT_EVENT)
    elif signum == 31:
        pygame.event.post(RIGHT_EVENT)
    elif signum == 28:
        pygame.event.post(SELECT_EVENT)

# def run_game():
signal.signal(signal.SIGUSR1, signal_handler)
signal.signal(signal.SIGUSR2, signal_handler)
signal.signal(signal.SIGWINCH, signal_handler)

print(2, os.getpid())
user_input = ""
current_word = ""
autocomplete_words = []
pre_auto = False
running = True
alpha = True
upper = False
cursor = KEYS.root

while running:

    # event handler
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == LEFT:
            if not alpha and cursor.left.is_leaf():
                cursor = KEYS.root
            elif cursor.is_leaf() or cursor.left.autocomplete == "":
                cursor = KEYS.root
            else:
                cursor = cursor.left

        elif event.type == RIGHT:
            if not alpha and cursor.right.is_leaf():
                cursor = KEYS.root
            elif cursor.is_leaf() or cursor.right.autocomplete == "":
                cursor = KEYS.root
            else:
                cursor = cursor.right

        elif event.type == SELECT:
            key = ""
            if alpha:
                key = cursor.alpha_key
                if key is None:
                    key = cursor.autocomplete
                    if not pre_auto:
                        user_input = (" ".join(user_input.split(" ")[:-1]) + " " + key).strip()
                    else:
                        user_input += " " + key
                    # current_word = ""
                    pre_auto = True
                else:
                    pre_auto = False
            else:
                key = cursor.punc_key
                pre_auto = False

            if len(key) == 1:
                if not upper and key.isalpha():
                    user_input += key.lower()
                    current_word += key.lower()
                else:
                    user_input += key
                    current_word += key
                    if not alpha:
                        current_word = ""
            elif key == "Space":
                user_input += " "
                current_word = ""
                print('reset')
            elif key == "Delete":
                user_input = user_input[:-1]
                current_word = current_word[:-1]
            elif key == "Clear":
                user_input = ""
                current_word = ""
            elif key == "U/L":
                upper = not upper
            elif key == "123":
                cursor = KEYS.root
                alpha = False
            elif key == "abc":
                upper = False
                cursor = KEYS.root
                alpha = True

        # move the cursor by key pressed
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                if not alpha and cursor.left.is_leaf():
                    cursor = KEYS.root
                elif cursor.is_leaf() or cursor.left.autocomplete == "":
                    cursor = KEYS.root
                else:
                    cursor = cursor.left

            if event.key == K_RIGHT:
                if not alpha and cursor.right.is_leaf():
                    cursor = KEYS.root
                elif cursor.is_leaf() or cursor.right.autocomplete == "":
                    cursor = KEYS.root
                else:
                    cursor = cursor.right

            if event.key == K_RETURN:
                key = ""
                if alpha:
                    key = cursor.alpha_key
                    if key is None:
                        key = cursor.autocomplete
                        if not pre_auto:
                            user_input = (" ".join(user_input.split(" ")[:-1]) + " " + key).strip()
                        else:
                            user_input += " " + key
                        # current_word = ""
                        pre_auto = True
                    else:
                        pre_auto = False
                else:
                    key = cursor.punc_key
                    pre_auto = False

                if len(key) == 1:
                    if not upper and key.isalpha():
                        user_input += key.lower()
                        current_word += key.lower()
                    else:
                        user_input += key
                        current_word += key
                        if not alpha:
                            current_word = ""
                elif key == "Space":
                    user_input += " "
                    current_word = ""
                    print('reset')
                elif key == "Delete":
                    user_input = user_input[:-1]
                    current_word = current_word[:-1]
                elif key == "Clear":
                    user_input = ""
                    current_word = ""
                elif key == "U/L":
                    upper = not upper
                elif key == "123":
                    cursor = KEYS.root
                    alpha = False
                elif key == "abc":
                    upper = False
                    cursor = KEYS.root
                    alpha = True

            if current_word != "":
                autocomplete_words = AUTOCOMPLETE.search(word=current_word, max_cost=3, size=16)
                # print(current_word, end=" ")
                # print(autocomplete_words)

        if current_word != "":
            autocomplete_words = AUTOCOMPLETE.search(word=current_word, max_cost=3, size=16)


    # fill the background with white
    SCREEN.fill(WHITE)

    # draw the text input box
    input_bar = pygame.Rect((INPUT_WIDTH, INPUT_HEIGHT), (595, 70))
    pygame.draw.rect(SCREEN, LIGHT_GREY, input_bar)
    input = INPUT_FONT.render(user_input, True, DARK_GREY)
    SCREEN.blit(input, (INPUT_WIDTH, INPUT_HEIGHT + 10))

    # BFS thru the nodes and draw the rectangles with the key
    fringe = [KEYS.root]
    i = j = k = 0  # i-height, j-width, k-autocomplete cursor
    while len(fringe) > 0:
        tmp = fringe.pop(0)

        if i == 5:
            tmp.width = LAYER_WIDTH[i][j//2]
            tmp.height = LAYER_HEIGHT[i]
        else:
            tmp.width = LAYER_WIDTH[i][j]
            tmp.height = LAYER_HEIGHT[i]

        tmp.rect = pygame.Rect((tmp.width, tmp.height), (RECT_X, RECT_Y))
        if not tmp.is_leaf():
            fringe.append(tmp.left)
            fringe.append(tmp.right)

        # draw the rectangle
        if not tmp.is_leaf():
            pygame.draw.rect(SCREEN, BLACK, tmp.rect, 1)
        else:
            if k < 2 * len(autocomplete_words) and alpha:
                tmp.autocomplete = autocomplete_words[k//2][0]
                pygame.draw.rect(SCREEN, BLACK, tmp.rect, 1)
                k += 1
            else:
                tmp.autocomplete = ""

        # draw the lines connecting to the children
        if not tmp.is_root() and tmp.autocomplete != "":
            start_pos = (tmp.width + 27.5, tmp.height)
            end_pos = (tmp.parent.width + 27.5, tmp.parent.height + 40)

            pygame.draw.line(SCREEN, BLACK, start_pos, end_pos)

        # create surface for keys
        rect_surf = pygame.Surface((RECT_X-2, RECT_Y-2))
        if cursor.width == tmp.width and cursor.height == tmp.height:
            rect_surf.fill(LIGHT_GREY)
        else:
            rect_surf.fill(WHITE)

        # key, option or autocomplete
        if alpha:
            key = tmp.alpha_key
            if key is None:
                key = tmp.autocomplete
                if key != "":
                    surface = AUTOCOMPLETE_FONT.render(key, True, DARK_GREY)
                    rect_surf.blit(surface, (1,8))
                    SCREEN.blit(rect_surf, (tmp.width + 1, tmp.height + 1))

            elif len(tmp.alpha_key) > 1:
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
            if tmp.is_leaf():
                continue
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
        if i != 5:
            if j >= len(LAYER_WIDTH[i]):
                i += 1
                j = 0
        # else:
        #     if j >= 2 * len(LAYER_WIDTH[i]):
        #         i += 1
        #         j = 0

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()