import pygame
from setting import *

class Node:
    def __init__(self, layer:int, height:int, width:int, alpha_key=None, punc_key=None, root=False, leaf=False):
        self.left_child = None
        self.right_child = None
        self.parent = None

        self.height = height
        self.width = width
        self.layer = layer

        self.leaf = leaf
        self.root = root
        self.selected = False

        self.alpha_key = alpha_key
        self.punc_key = punc_key
    
    def is_leaf(self):
        return self.leaf
    
    def is_root(self):
        return self.root
    
    def set_height(self, height):
        self.height = height

    def get_height(self):
        return self.height
    
    def set_width(self, width):
        self.width = width

    def get_width(self):
        return self.width

    def get_alpha_key(self):
        return self.alpha_key

    def get_punc_key(self):
        return self.punc_key
    
    def select(self):
        self.selected = True

    def not_select(self):
        self.selected = False

    def get_layer(self):
        return self.layer

    def get_left(self):
        return self.left_child

    def set_left(self, left):
        self.left_child = left

    def get_right(self):
        return self.right_child
    
    def set_right(self, right):
        self.right_child = right

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def render(self, SCREEN, alpha, upper, p):
        # draw the rectangle
        rect = p.Rect((self.width, self.height), (NODE_LENGTH, NODE_LENGTH))
        p.draw.rect(SCREEN, BLACK, rect, 1)

        # draw the lines connecting to children if not a leaf
        if not self.is_leaf():
            start = (self.width + NODE_LENGTH/2, self.height + NODE_LENGTH)
            end_left = (self.left_child.width + NODE_LENGTH/2, self.left_child.height)
            end_right = (self.right_child.width + NODE_LENGTH/2, self.right_child.height)

            p.draw.line(SCREEN, BLACK, start, end_left)
            p.draw.line(SCREEN, BLACK, start, end_right)

        # fill the node
        rect_surf = p.Surface((NODE_LENGTH-2, NODE_LENGTH-2))
        if self.selected:
            rect_surf.fill(LIGHT_GREY)
        else:
            rect_surf.fill(WHITE)

        if self.is_leaf():
            if alpha:
                key = self.alpha_key
                
                if len(key) > 1:
                    # options
                    if key == "U/L":
                        if upper:
                            key = "Lower"
                        else:
                            key = "Upper"
                    surface = p.font.Font(None, 15).render(key, True, DARK_GREY)
                    if len(key) == 5:
                        rect_surf.blit(surface, (1, 10))
                    elif len(key) == 3:
                        rect_surf.blit(surface, (8, 10))
                    else:
                        rect_surf.blit(surface, (0, 10))

                    SCREEN.blit(rect_surf, (self.width + 1, self.height + 1))
                
                else:
                    # alphabets
                    if not upper:
                        key = key.lower()

                    surface = p.font.Font(None, 45).render(key, True, DARK_GREY)
                    rect_surf.blit(surface, (8, 2))
                    SCREEN.blit(rect_surf, (self.width + 1, self.height + 1))
            
            else:
                if len(str(self.punc_key)) > 1:
                    surface = p.font.Font(None, 15).render(self.punc_key, True, DARK_GREY)

                    if len(self.punc_key) == 5:
                        rect_surf.blit(surface, (1, 10))
                    elif len(self.punc_key) == 3:
                        rect_surf.blit(surface, (8, 10))
                    else:
                        rect_surf.blit(surface, (0, 10))

                    SCREEN.blit(rect_surf, (self.width + 1, self.height + 1))
                else:
                    surface = p.font.Font(None, 40).render(self.punc_key, True, DARK_GREY)
                    rect_surf.blit(surface, (8, 2))
                    SCREEN.blit(rect_surf, (self.width + 1, self.height + 1))                
        else:
            SCREEN.blit(rect_surf, (self.width + 1, self.height + 1))
        
