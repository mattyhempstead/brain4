import pygame, math
from Node import Node
from setting import *

class Tree:
    def __init__(self):
        self.root = None
        self.alpha_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Space', '123', 'U/L', 'Delete', 'Clear', 'Return']
        self.punc_keys = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ',', ':', ';', '/', '?', '!', '\'', '\"', '@', '&', '-', '_', '(', ')', '[', ']', 'Space', 'ABC', 'Delete', 'Clear', 'Return']
    
    def get_root(self):
        return self.root

    def init_trees(self):
        key_cursor = 0
        width_cursor = 0

        self.root = Node(1, LAYER_HEIGHT[0], LAYER_WIDTH[0][0], root=True)

        tmp = [self.root]
        while len(tmp) > 0:
            cur = tmp[0]

            # create a new node
            new = None

            height = LAYER_HEIGHT[cur.get_layer()]
            if cur.get_layer() == TREE_LAYER-1:
                if width_cursor % 2 == 0:
                    height = LAYER_HEIGHT[cur.get_layer()][(width_cursor//2)%2]
                else:
                    height = LAYER_HEIGHT[cur.get_layer()][((width_cursor-1)//2)%2]

            width = LAYER_WIDTH[cur.get_layer()][width_cursor]
            
            if width_cursor >= math.pow(2, cur.get_layer())-1:
                width_cursor = 0
            else:
                width_cursor += 1

            if cur.get_layer() == TREE_LAYER-1:
                new = Node(TREE_LAYER, height, width, alpha_key=self.alpha_keys[key_cursor], punc_key=self.punc_keys[key_cursor], leaf=True)
                key_cursor += 1
            else:
                new = Node(cur.get_layer()+1, height, width)
                tmp.append(new)
            
            # set parent and children
            new.set_parent(cur)
            if cur.get_left() is None:
                cur.set_left(new)
            elif cur.get_right() is None:
                cur.set_right(new)
                tmp.pop(0)

    def render(self, alpha, upper):
        fringe = [self.root]

        while len(fringe) > 0:
            tmp = fringe.pop(0)
            tmp.render(alpha, upper)

            if not tmp.is_leaf():
                fringe.append(tmp.get_left())
                fringe.append(tmp.get_right())

    def print_tree(self):
        fringe = [self.root]
        
        while len(fringe) > 0:
            tmp = fringe.pop(0)
            print(tmp.alpha_key, tmp.punc_key)
            print(tmp.height, tmp.width)
            
            if not tmp.is_leaf():
                fringe.append(tmp.left_child)
                fringe.append(tmp.right_child)
