from setting import *
from text import draw_text
from typing import Tuple

class ACNode:
    WIDTH = 80
    HEIGHT = 45

    BORDER_RADIUS = 10
    BORDER_COLOR = BLACK

    BACKGROUND_COLOR = WHITE
    BACKGROUND_COLOR_LEAF = (247, 246, 220)
    BACKGROUND_COLOR_SELECTED = (171,188,214)

    EDGE_TEXT_FONT_SIZE = 22
    EDGE_TEXT_CIRCLE_RADIUS = 10
    EDGE_TEXT_CIRCLE_COLOR = (185, 222, 240)
    EDGE_TEXT_CIRCLE_BORDER_COLOR = BLACK

    def __init__(self, layer:int, height:int, width:int, key="None", root=False, leaf=False):
        self.left_child = None
        self.right_child = None
        self.parent = None

        self.height = height
        self.width = width
        self.layer = layer

        self.leaf = leaf
        self.root = root   
        self.selected = False

        self.key = key

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

    def get_key(self):
        return self.key

    def set_key(self, word):
        self.key = word
    
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

    @property
    def rect(self):
        return pygame.Rect(
            (self.width, self.height),
            (ACNode.WIDTH, ACNode.HEIGHT),
        )

    def render(self):
        self.render_rect()
        self.render_edges()
        self.render_text()
    
    def render_rect(self):
        fill_colour = ACNode.BACKGROUND_COLOR
        if self.leaf:
            fill_colour = ACNode.BACKGROUND_COLOR_LEAF
        if self.selected:
            fill_colour = ACNode.BACKGROUND_COLOR_SELECTED
        pygame.draw.rect(SCREEN, fill_colour, self.rect, 0, ACNode.BORDER_RADIUS)
        pygame.draw.rect(SCREEN, ACNode.BORDER_COLOR, self.rect, 2, ACNode.BORDER_RADIUS)

    def render_edges(self):
        if self.is_leaf():
            return
        
        start = self.rect.midbottom
        end_left = self.left_child.rect.midtop
        end_right = self.right_child.rect.midtop

        pygame.draw.line(SCREEN, BLACK, start, end_left)
        pygame.draw.line(SCREEN, BLACK, start, end_right)        

        if self.selected: 
            edge_left_midpoint = (
                (start[0] + end_left[0]) / 2,
                (start[1] + end_left[1]) / 2,
            )
            self.render_edge_text("L", edge_left_midpoint)

            edge_right_midpoint = (
                (start[0] + end_right[0]) / 2,
                (start[1] + end_right[1]) / 2,
            )
            self.render_edge_text("R", edge_right_midpoint)

            if self.parent is not None:
                edge_parent_midpoint = (
                    (self.rect.midtop[0] + self.parent.rect.midbottom[0]) / 2,
                    (self.rect.midtop[1] + self.parent.rect.midbottom[1]) / 2,
                )
                self.render_edge_text("B", edge_parent_midpoint)


    def render_edge_text(self, text:str, pos:Tuple[int,int]):
        # Circle background
        pygame.draw.circle(
            SCREEN, 
            ACNode.EDGE_TEXT_CIRCLE_COLOR,
            pos, 
            ACNode.EDGE_TEXT_CIRCLE_RADIUS
        )

        # Circle border
        pygame.draw.circle(
            SCREEN, 
            ACNode.EDGE_TEXT_CIRCLE_BORDER_COLOR,
            pos, 
            ACNode.EDGE_TEXT_CIRCLE_RADIUS,
            1
        )

        # Text
        draw_text(
            text = text,
            pos = pos,
            size = ACNode.EDGE_TEXT_FONT_SIZE,
            color = DARK_GREY
        )

    def render_text(self):
        rect_surf = pygame.Surface((ACNode.WIDTH-2, ACNode.HEIGHT-2), pygame.SRCALPHA, 32)
        rect_surf = rect_surf.convert_alpha()

        if self.is_leaf():
            surface = pygame.font.Font(None, 18).render(self.key, True, DARK_GREY)
            if len(self.key) <= 5:
                rect_surf.blit(surface, (25, 15))
            elif len(self.key) <= 10:
                rect_surf.blit(surface, (20, 15))
            else:
                rect_surf.blit(surface, (10, 15))
        
        SCREEN.blit(rect_surf, (self.width + 1, self.height + 1))
