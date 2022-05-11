# Import and initialize the pygame library
import pygame, os, signal
import csv

from setting import *
from Tree import Tree
from InputBox import InputBox

from brainbox.brainbox import brainbox_loop

class App:
    BACKGROUND_COLOR = LIGHT_GREY

    KEYLOG_MODE = False

    def __init__(self):
        print(2, os.getpid())

        self.running = True
        self.alpha = True
        self.upper = False

        self.user_input = ""
        self.current_word = ""
        self.autocomplete_words = []
        self.pre_auto = False

        self.tree = Tree()
        self.tree.init_trees()
        self.cursor = self.tree.get_root()
        self.cursor.select()
        
        self.input_box = InputBox()
        
        # self.key_logger = KeyLogger()


    def start(self):
        self.clock = pygame.time.Clock()

        while self.running:
            
            brainbox_loop()

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
                    # move the cursor by keypresses
                    self.event_keydown(event)
                
                if self.current_word != "":
                    self.autocomplete_words = AUTOCOMPLETE.search(word=self.current_word, max_cost=3, size=16)

            self.render()

            if FPS is not None:
                self.clock.tick(FPS)

        # Done! Time to quit.
        pygame.quit()

        # self.key_logger.close()


    def event_quit(self):
        self.running = False

    def event_left(self):
        if App.KEYLOG_MODE:
            # self.key_logger.write("L")
            return


        # if not self.alpha and self.cursor.left.is_leaf():
        #     self.cursor = KEYS.root
        # elif self.cursor.is_leaf() or self.cursor.left.autocomplete == "":
        #     self.cursor = KEYS.root
        # else:
        #     self.cursor = self.cursor.left
        self.cursor.not_select()
        if self.cursor.is_leaf():
            self.cursor = self.tree.get_root()
        else:
            self.cursor = self.cursor.get_left()
        self.cursor.select()
        

    def event_right(self):
        if App.KEYLOG_MODE:
            # self.key_logger.write("R")
            return

        # if not self.alpha and self.cursor.right.is_leaf():
        #     self.cursor = KEYS.root
        # elif self.cursor.is_leaf() or self.cursor.right.autocomplete == "":
        #     self.cursor = KEYS.root
        # else:
        #     self.cursor = self.cursor.right
        self.cursor.not_select()
        if self.cursor.is_leaf():
            self.cursor = self.tree.get_root()
        else:
            self.cursor = self.cursor.get_right()
        self.cursor.select()


    def event_select(self):
        if App.KEYLOG_MODE:
            # self.key_logger.write("S")
            return

        key = ""

        # move back if not a leaf
        if not self.cursor.is_leaf():
            if self.cursor.is_root():
                return
            self.cursor.not_select()
            self.cursor = self.cursor.get_parent()
            self.cursor.select()
            return
        
        if self.alpha:
            key = self.cursor.get_alpha_key()
            # if key is None:
            #     key = self.cursor.autocomplete
            #     if not self.pre_auto:
            #         self.user_input = (" ".join(self.user_input.split(" ")[:-1]) + " " + key).strip()
            #     else:
            #         self.user_input += " " + key
            #     # self.current_word = ""
            #     self.pre_auto = True
            # else:
            #     self.pre_auto = False
        else:
            key = self.cursor.get_punc_key()
            self.pre_auto = False

        if len(key) == 1:
            if not self.upper and key.isalpha():
                self.input_box.append_text(key.lower())
                self.current_word += key.lower()
            else:
                self.input_box.append_text(key)
                self.current_word += key
                if not self.alpha:
                    self.current_word = ""
        elif key == "Space":
            self.input_box.append_text(" ")
            self.current_word = ""
        elif key == "Delete":
            self.input_box.delete_text()
            self.current_word = self.current_word[:-1]
        elif key == "Return":
            self.input_box.new_line()
        elif key == "Clear":
            self.input_box.clear_text()
            self.current_word = ""
        elif key == "U/L":
            self.upper = not self.upper
        elif key == "123":
            self.cursor.not_select()
            self.cursor = KEYS.root
            self.cursor.select()
            self.alpha = False
        elif key == "ABC":
            self.upper = False
            self.cursor.not_select()
            self.cursor = KEYS.root
            self.cursor.select()
            self.alpha = True


    def event_keydown(self, event):
        if event.key == K_LEFT:
            self.cursor.not_select()
            if self.cursor.is_leaf():
                self.cursor = self.tree.get_root()
            else:
                self.cursor = self.cursor.get_left()
            self.cursor.select()

        elif event.key == K_RIGHT:
            self.cursor.not_select()
            if self.cursor.is_leaf():
                self.cursor = self.tree.get_root()
            else:
                self.cursor = self.cursor.get_right()
            self.cursor.select()

        elif event.key == K_RETURN:
            key = ""

            # move back if not a leaf
            if not self.cursor.is_leaf():
                if self.cursor.is_root():
                    return
                self.cursor.not_select()
                self.cursor = self.cursor.get_parent()
                self.cursor.select()
                return
            
            if self.alpha:
                key = self.cursor.get_alpha_key()
                # if key is None:
                #     key = self.cursor.autocomplete
                #     if not self.pre_auto:
                #         self.user_input = (" ".join(self.user_input.split(" ")[:-1]) + " " + key).strip()
                #     else:
                #         self.user_input += " " + key
                #     # self.current_word = ""
                #     self.pre_auto = True
                # else:
                #     self.pre_auto = False
            else:
                key = self.cursor.get_punc_key()
                self.pre_auto = False

            if len(key) == 1:
                if not self.upper and key.isalpha():
                    self.input_box.append_text(key.lower())
                    self.current_word += key.lower()
                else:
                    self.input_box.append_text(key)
                    self.current_word += key
                    if not self.alpha:
                        self.current_word = ""
            elif key == "Space":
                self.input_box.append_text(" ")
                self.current_word = ""
            elif key == "Delete":
                self.input_box.delete_text()
                self.current_word = self.current_word[:-1]
            elif key == "Return":
                self.input_box.new_line()
            elif key == "Clear":
                self.input_box.clear_text()
                self.current_word = ""
            elif key == "U/L":
                self.upper = not self.upper
            elif key == "123":
                self.alpha = False
            elif key == "ABC":
                self.upper = False
                self.alpha = True
                
            self.cursor.not_select()
            self.cursor = self.tree.get_root()
            self.cursor.select()

        # if self.current_word != "":
        #     self.autocomplete_words = AUTOCOMPLETE.search(word=self.current_word, max_cost=3, size=16)
            # print(self.current_word, end=" ")
            # print(self.autocomplete_words)


    def render(self):

        # fill the background with white
        SCREEN.fill(App.BACKGROUND_COLOR)

        # draw the text input box
        self.input_box.render()

        self.tree.render(self.alpha, self.upper)

        # Flip the display
        pygame.display.flip()


    # def draw_text_input_box(self):
    #     input_bar = pygame.Rect((INPUT_WIDTH, INPUT_HEIGHT), (595, 70))
    #     pygame.draw.rect(SCREEN, LIGHT_GREY, input_bar)
    #     input = INPUT_FONT.render(self.user_input, True, DARK_GREY)
    #     SCREEN.blit(input, (INPUT_WIDTH, INPUT_HEIGHT + 10))
    

    # def draw_tree(self):
    #     i = j = 0

    #     while True:
    #         tmp = KEYS.root
    #         self.draw_tree_node(tmp, i, j)

    #         j += 1
    #         if i != NUM_LAYER-1:
    #             if j >= len(LAYER_WIDTH[i]):
    #                 i += 1
    #                 j = 0
    #         else:
    #             if j >= len(LAYER_WIDTH[i]):
    #                 return

    #     # BFS thru the nodes and draw the rectangles with the key
    #     fringe = [KEYS.root]

    #     i = j = 0  # i-height, j-width

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


    # def draw_tree_node(self, tmp, i, j):
    #     if i == NUM_LAYER-1:
    #         tmp.width = LAYER_WIDTH[i][j]
    #         print(tmp.width)
    #         if j % 2 == 0:
    #             tmp.height = LAYER_HEIGHT[i][(j//2)%2]
    #             print(tmp.height)
    #         else:
    #             tmp.height = LAYER_HEIGHT[i][((j-1)//2)%2]
    #             print(tmp.height)
    #     else:
    #         tmp.width = LAYER_WIDTH[i][j]
    #         tmp.height = LAYER_HEIGHT[i]
        

    #     tmp.rect = pygame.Rect((tmp.width, tmp.height), (RECT_X, RECT_Y))
    #     pygame.draw.rect(SCREEN, BLACK, tmp.rect, 1)

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

