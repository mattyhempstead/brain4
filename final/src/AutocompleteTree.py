import math
from ACNode import ACNode
from setting import *

class AutocompleteTree:
    def __init__(self):
        self.root = ""
        self.leaves = []

    def init_trees(self):
        width_cursor = 0

        self.root = ACNode(1, LAYER_HEIGHT[0], LAYER_WIDTH[0][0], root = True)

        tmp = [self.root]
        while len(tmp) > 0:
            cur = tmp[0]

            height = LAYER_HEIGHT[cur.get_layer()]
            width = LAYER_WIDTH[cur.get_layer()][width_cursor]

            if width_cursor >= math.pow(2, cur.get_layer())-1:
                width_cursor = 0
            else:
                width_cursor += 1

            if cur.get_layer() != AUTOCOMPLETE_LAYER-1:
                new = ACNode(cur.get_layer()+1, height, width)
                tmp.append(new)
            else:                
                new = ACNode(cur.get_layer()+1, height, width, leaf=True)
                self.leaves.append(new)
            
            new.set_parent(cur)
            if cur.get_left() is None:
                cur.set_left(new)
            elif cur.get_right() is None:
                cur.set_right(new)
                tmp.pop(0)

    def get_root(self):
        return self.root

    def reset_keys(self):
        for leaf in self.leaves:
            leaf.set_key("")

    def render(self):
        fringe = [self.root]

        while len(fringe) > 0:
            tmp = fringe.pop(0)
            tmp.render()

            if not tmp.is_leaf():
                fringe.append(tmp.get_left())
                fringe.append(tmp.get_right())
    
    def refresh(self, user_input):
        words = AUTOCOMPLETE.search(word=user_input, max_cost=3, size=8)
        self.reset_keys()
        cursor = 0
        for word in words:
            self.leaves[cursor].set_key(word[0])
            cursor += 1
        
