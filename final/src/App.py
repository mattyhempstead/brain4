# Import and initialize the pygame library
import pygame, os, signal
import csv

from setting import *
from KeyboardTree import KeyboardTree
from AutocompleteTree import AutocompleteTree
from SwitchCircle import SwitchCircle
from InputBox import InputBox

from brainbox.brainbox import brainbox_loop

class App:
    BACKGROUND_COLOR = LIGHT_GREY

    KEYLOG_MODE = False

    def __init__(self):

        self.kbtree = KeyboardTree()
        self.kbtree.init_trees()
        self.cursor = self.kbtree.get_root()
        self.cursor.select()

        self.actree = AutocompleteTree()
        self.actree.init_trees()
        self.current_word = ""
        self.pre_auto = False

        self.circle = SwitchCircle()
        self.circle.init_circle()

        self.running = True
        self.alpha = True
        self.upper = False
        self.autocomplete = False
        self.switching = False
        
        self.input_box = InputBox()
        
        # self.key_logger = KeyLogger()

        # self.running = True
        # self.alpha = True
        # self.upper = False

        # self.user_input = ""
        # self.current_word = ""
        # self.autocomplete_words = []
        # self.pre_auto = False

        # self.tree = Tree()
        # self.tree.init_trees()
        # self.cursor = self.tree.get_root()
        # self.cursor.select()
        
        # self.input_box = InputBox()
        
        # # self.key_logger = KeyLogger()


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
                
            self.render()

            if FPS is not None:
                self.clock.tick(FPS)

        # Done! Time to quit.
        pygame.quit()

        # self.key_logger.close()


    def switch_cursor(self, new):
        self.cursor.not_select()
        self.cursor = new
        self.cursor.select()
        # self.key_logger.close()


    def event_quit(self):
        self.running = False

    def event_left(self):
        if App.KEYLOG_MODE:
            # self.key_logger.write("L")
            return

        if self.switching:
            self.circle.set_keys(self.circle.get_current_idx()+1)
            self.switch_cursor(self.circle.get_current_mode())
            return

        if self.cursor.is_leaf():
            if self.autocomplete:
                self.switch_cursor(self.actree.get_root())
            else:
                self.switch_cursor(self.kbtree.get_root())
        else:
            self.switch_cursor(self.cursor.get_left())
        

    def event_right(self):
        if App.KEYLOG_MODE:
            # self.key_logger.write("R")
            return

        if self.switching:
            self.circle.set_keys(self.circle.get_current_idx()-1)
            self.switch_cursor(self.circle.get_current_mode())
            return

        if self.cursor.is_leaf():
            if self.autocomplete:
                self.switch_cursor(self.actree.get_root())
            else:
                self.switch_cursor(self.kbtree.get_root())
        else:
            self.switch_cursor(self.cursor.get_right())


    def event_select(self):
        if App.KEYLOG_MODE:
            # self.key_logger.write("S")
            return

        if self.switching:
            self.autocomplete = False

            key = self.cursor.get_key()
            if key == "Lowercase":
                self.alpha = True
                self.upper = False
                self.switch_cursor(self.kbtree.get_root())
            elif key == "Uppercase":
                self.alpha = True
                self.upper = True
                self.switch_cursor(self.kbtree.get_root())
            elif key == "Punctuation":
                self.alpha = False
                self.switch_cursor(self.kbtree.get_root())
            elif key == "Autocomplete":
                self.autocomplete = True
                self.switch_cursor(self.actree.get_root())

            self.switching = False
            self.circle.set_keys(0)
            return

        # switching trees
        if self.cursor.is_root():
            self.switching = True
            self.switch_cursor(self.circle.get_current_mode())
            return

        # move back if not a leaf
        if not self.cursor.is_leaf():
            self.switch_cursor(self.cursor.get_parent())
            return

        if self.autocomplete:
            key = self.cursor.get_key()
            # if not self.pre_auto:
            input = self.input_box.get_user_input()[-1]
            self.input_box.set_text((" ".join(input.split(" ")[:-1]) + " " + key).strip())
            # else:
            #     self.user_input += " " + key
            #     print(self.user_input)
            self.current_word = ""
            # self.pre_auto = True
            self.switch_cursor(self.kbtree.get_root())
            self.autocomplete = False
            return
        
        # self.pre_auto = False
        
        key = ""
        if self.alpha:
            key = self.cursor.get_alpha_key()
        else:
            key = self.cursor.get_punc_key()

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
            self.current_word = ""
        elif key == "Clear":
            self.input_box.clear_text()
            self.current_word = ""
        elif key == "U/L":
            self.upper = not self.upper
        elif key == "Tab":
            self.input_box.append_text("    ")
            self.current_word = ""
        elif key == "ABC":
            self.upper = False
            self.alpha = True

        self.switch_cursor(self.kbtree.get_root())

    def event_keydown(self, event):
        if event.key == K_LEFT:
            self.event_left()

        elif event.key == K_RIGHT:
            self.event_right()

        elif event.key == K_RETURN:
            self.event_select()

    def render(self):

        # fill the background with white
        SCREEN.fill(App.BACKGROUND_COLOR)

        # draw the text input box
        self.input_box.render()

        if self.switching:
            self.circle.render()
        elif self.autocomplete:
            self.actree.refresh(self.current_word)
            self.actree.render()
        else:
            self.kbtree.render(self.alpha, self.upper)

        # Flip the display
        pygame.display.flip()


 