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
WIDTH, HEIGHT = 1455, 800
RECT_X, RECT_Y = 35, 35
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
LAYER_HEIGHT = [150, 240, 330, 420, 510, [600, 650], 740]
LAYER_WIDTH = [[700],
               [500, 900],
               [340, 590, 790, 1060],
               [200, 350, 500, 625, 775, 900, 1050, 1200],
               [80, 160, 240, 320, 400, 480, 560, 640, 760, 840, 920, 1000, 1080, 1160, 1240, 1320],
               [20, 70, 115, 165, 205, 255, 295, 340, 380, 420, 465, 505, 550, 595, 640, 685, 715, 760, 805, 850, 895, 935, 980, 1020, 1060, 1105, 1145, 1195, 1235, 1285, 1330, 1380]]

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


FPS = 30  # None for unlimited


class App:
    def __init__(self):
        print(2, os.getpid())

        self.running = True
        self.user_input = ""
        self.current_word = ""
        self.autocomplete_words = []
        self.pre_auto = False
        self.alpha = True
        self.upper = False
        self.cursor = KEYS.root



    def start(self):
        self.clock = pygame.time.Clock()

        signal.signal(signal.SIGUSR1, signal_handler)
        signal.signal(signal.SIGUSR2, signal_handler)
        signal.signal(signal.SIGWINCH, signal_handler)

        while self.running:

            # event handler
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.event_quit()
                elif event.type == LEFT:
                    self.event_left()
                elif event.type == RIGHT:
                    self.event_right()
                elif event.type == SELECT:
                    self.event_select()
                elif event.type == KEYDOWN:
                    # move the cursor by key pressed
                    self.event_keydown(event)
                
                if self.current_word != "":
                    self.autocomplete_words = AUTOCOMPLETE.search(word=self.current_word, max_cost=3, size=16)

            self.render()

        # Done! Time to quit.
        pygame.quit()


    def event_quit(self):
        self.running = False

    def event_left(self):
        if not self.alpha and self.cursor.left.is_leaf():
            self.cursor = KEYS.root
        elif self.cursor.is_leaf() or self.cursor.left.autocomplete == "":
            self.cursor = KEYS.root
        else:
            self.cursor = self.cursor.left

    def event_right(self):
        if not self.alpha and self.cursor.right.is_leaf():
            self.cursor = KEYS.root
        elif self.cursor.is_leaf() or self.cursor.right.autocomplete == "":
            self.cursor = KEYS.root
        else:
            self.cursor = self.cursor.right

    def event_select(self):
        key = ""
        if self.alpha:
            key = self.cursor.alpha_key
            if key is None:
                key = self.cursor.autocomplete
                if not self.pre_auto:
                    self.user_input = (" ".join(self.user_input.split(" ")[:-1]) + " " + key).strip()
                else:
                    self.user_input += " " + key
                # self.current_word = ""
                self.pre_auto = True
            else:
                self.pre_auto = False
        else:
            key = self.cursor.punc_key
            self.pre_auto = False

        if len(key) == 1:
            if not self.upper and key.isalpha():
                self.user_input += key.lower()
                self.current_word += key.lower()
            else:
                self.user_input += key
                self.current_word += key
                if not self.alpha:
                    self.current_word = ""
        elif key == "Space":
            self.user_input += " "
            self.current_word = ""
            print('reset')
        elif key == "Delete":
            self.user_input = self.user_input[:-1]
            self.current_word = self.current_word[:-1]
        elif key == "Clear":
            self.user_input = ""
            self.current_word = ""
        elif key == "U/L":
            self.upper = not self.upper
        elif key == "123":
            self.cursor = KEYS.root
            self.alpha = False
        elif key == "abc":
            self.upper = False
            self.cursor = KEYS.root
            self.alpha = True

    def event_keydown(self, event):

        if event.key == K_LEFT:
            if not self.alpha and self.cursor.left.is_leaf():
                self.cursor = KEYS.root
            elif self.cursor.is_leaf() or self.cursor.left.autocomplete == "":
                self.cursor = KEYS.root
            else:
                self.cursor = self.cursor.left

        if event.key == K_RIGHT:
            if not self.alpha and self.cursor.right.is_leaf():
                self.cursor = KEYS.root
            elif self.cursor.is_leaf() or self.cursor.right.autocomplete == "":
                self.cursor = KEYS.root
            else:
                self.cursor = self.cursor.right

        if event.key == K_RETURN:
            key = ""
            if self.alpha:
                key = self.cursor.alpha_key
                if key is None:
                    key = self.cursor.autocomplete
                    if not self.pre_auto:
                        self.user_input = (" ".join(self.user_input.split(" ")[:-1]) + " " + key).strip()
                    else:
                        self.user_input += " " + key
                    # self.current_word = ""
                    self.pre_auto = True
                else:
                    self.pre_auto = False
            else:
                key = self.cursor.punc_key
                self.pre_auto = False

            if len(key) == 1:
                if not self.upper and key.isalpha():
                    self.user_input += key.lower()
                    self.current_word += key.lower()
                else:
                    self.user_input += key
                    self.current_word += key
                    if not self.alpha:
                        self.current_word = ""
            elif key == "Space":
                self.user_input += " "
                self.current_word = ""
                print('reset')
            elif key == "Delete":
                self.user_input = self.user_input[:-1]
                self.current_word = self.current_word[:-1]
            elif key == "Clear":
                self.user_input = ""
                self.current_word = ""
            elif key == "U/L":
                self.upper = not self.upper
            elif key == "123":
                self.cursor = KEYS.root
                self.alpha = False
            elif key == "abc":
                self.upper = False
                self.cursor = KEYS.root
                self.alpha = True

        if self.current_word != "":
            self.autocomplete_words = AUTOCOMPLETE.search(word=self.current_word, max_cost=3, size=16)
            # print(self.current_word, end=" ")
            # print(self.autocomplete_words)


    def render(self):

        # fill the background with white
        SCREEN.fill(WHITE)

        # draw the text input box
        self.draw_text_input_box()

        self.draw_tree()

        if FPS is not None:
            self.clock.tick(FPS)

        # Flip the display
        pygame.display.flip()


    def draw_text_input_box(self):
        input_bar = pygame.Rect((INPUT_WIDTH, INPUT_HEIGHT), (595, 70))
        pygame.draw.rect(SCREEN, LIGHT_GREY, input_bar)
        input = INPUT_FONT.render(self.user_input, True, DARK_GREY)
        SCREEN.blit(input, (INPUT_WIDTH, INPUT_HEIGHT + 10))


    def draw_tree(self):
        i = j = 0

        while True:
            tmp = KEYS.root
            self.draw_tree_node(tmp, i, j)

            j += 1
            if i != NUM_LAYER-1:
                if j >= len(LAYER_WIDTH[i]):
                    i += 1
                    j = 0
            else:
                if j >= len(LAYER_WIDTH[i]):
                    return

        # BFS thru the nodes and draw the rectangles with the key
        fringe = [KEYS.root]

        i = j = 0  # i-height, j-width

        # Pop each word as we use it
        # Temp hack gives (a,b,c) -> (a,a,b,b,c,c)
        # self.tmp_ac_words = self.autocomplete_words
        # self.tmp_ac_words = list(sum(zip(self.tmp_ac_words, self.tmp_ac_words),()))

        # while len(fringe) > 0:
        #     tmp = fringe.pop(0)
        #     if not tmp.is_leaf():
        #         fringe.append(tmp.left)
        #         fringe.append(tmp.right)

        #     self.draw_tree_node(tmp, i, j)

        #     j += 1
        #     if i != NUM_LAYER-1:
        #         if j >= len(LAYER_WIDTH[i]):
        #             i += 1
        #             j = 0


    def draw_tree_node(self, tmp, i, j):
        if i == NUM_LAYER-1:
            tmp.width = LAYER_WIDTH[i][j]
            print(tmp.width)
            if j % 2 == 0:
                tmp.height = LAYER_HEIGHT[i][(j//2)%2]
                print(tmp.height)
            else:
                tmp.height = LAYER_HEIGHT[i][((j-1)//2)%2]
                print(tmp.height)
        else:
            tmp.width = LAYER_WIDTH[i][j]
            tmp.height = LAYER_HEIGHT[i]
        

        tmp.rect = pygame.Rect((tmp.width, tmp.height), (RECT_X, RECT_Y))
        pygame.draw.rect(SCREEN, BLACK, tmp.rect, 1)

        # draw the rectangle
        # if not tmp.is_leaf():
        #     pygame.draw.rect(SCREEN, BLACK, tmp.rect, 1)
        # else:
        #     # if k < 2 * len(self.autocomplete_words) and self.alpha:
        #     if len(self.tmp_ac_words) > 0:
        #         tmp.autocomplete = self.tmp_ac_words.pop()[0]
        #         pygame.draw.rect(SCREEN, BLACK, tmp.rect, 1)
        #     else:
        #         tmp.autocomplete = ""

        # # draw the lines connecting to the children
        # if not tmp.is_root() and tmp.autocomplete != "":
        #     start_pos = (tmp.width + 27.5, tmp.height)
        #     end_pos = (tmp.parent.width + 27.5, tmp.parent.height + 40)

        #     pygame.draw.line(SCREEN, BLACK, start_pos, end_pos)

        # # create surface for keys
        # rect_surf = pygame.Surface((RECT_X-2, RECT_Y-2))
        # if self.cursor.width == tmp.width and self.cursor.height == tmp.height:
        #     rect_surf.fill(LIGHT_GREY)
        # else:
        #     rect_surf.fill(WHITE)

        # key, option or autocomplete
        # if self.alpha:
        #     key = tmp.alpha_key
        #     if key is None:
        #         key = tmp.autocomplete
        #         if key != "":
        #             surface = AUTOCOMPLETE_FONT.render(key, True, DARK_GREY)
        #             rect_surf.blit(surface, (1,8))
        #             SCREEN.blit(rect_surf, (tmp.width + 1, tmp.height + 1))

        #     elif len(tmp.alpha_key) > 1:
        #         if key == "U/L":
        #             if self.upper:
        #                 key = "Lower"
        #             else:
        #                 key = "Upper"
        #         surface = OPTION_FONT.render(key, True, DARK_GREY)

        #         if len(key) == 5:
        #             rect_surf.blit(surface, (1, 8))
        #         elif len(key) == 3:
        #             rect_surf.blit(surface, (8, 8))
        #         else:
        #             rect_surf.blit(surface, (0, 8))

        #         SCREEN.blit(rect_surf, (tmp.width + 1, tmp.height + 1))
        #     else:
        #         if not self.upper:
        #             key = key.lower()

        #         surface = KEY_FONT.render(key, True, DARK_GREY)
        #         rect_surf.blit(surface, (16, 4))
        #         SCREEN.blit(rect_surf, (tmp.width + 1, tmp.height + 1))
        # else:
            # if tmp.is_leaf():
            #     return
            # if len(str(tmp.punc_key)) > 1:
            #     surface = OPTION_FONT.render(tmp.punc_key, True, DARK_GREY)

            #     if len(tmp.punc_key) == 5:
            #         rect_surf.blit(surface, (1, 8))
            #     elif len(tmp.punc_key) == 3:
            #         rect_surf.blit(surface, (8, 8))
            #     else:
            #         rect_surf.blit(surface, (0, 8))

            #     SCREEN.blit(rect_surf, (tmp.width + 1, tmp.height + 1))
            # else:
            #     surface = KEY_FONT.render(str(tmp.punc_key), True, DARK_GREY)
            #     rect_surf.blit(surface, (15, 4))
            #     SCREEN.blit(rect_surf, (tmp.width + 1, tmp.height + 1))




app = App()
app.start()
