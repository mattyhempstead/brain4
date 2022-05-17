from setting import *

class ModeNode:
    WIDTH = 125
    HEIGHT = 50

    BORDER_RADIUS = 10
    BORDER_COLOR = BLACK

    BACKGROUND_COLOR = (247, 246, 220)
    BACKGROUND_COLOR_SELECTED = (171,188,214)

    EDGE_TEXT_FONT_SIZE = 22
    EDGE_TEXT_CIRCLE_RADIUS = 10
    EDGE_TEXT_CIRCLE_COLOR = (185, 222, 240)
    EDGE_TEXT_CIRCLE_BORDER_COLOR = BLACK

    def __init__(self, height:int, width:int):
        self.key = None

        self.height = height
        self.width = width

        self.selected = False

    def get_left(self):
        return self.left

    def set_left(self, left):
        self.left = left

    def get_right(right):
        return self.right

    def set_right(self, right):
        self.right = right

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def select(self):
        self.selected = True
    
    def not_select(self):
        self.selected = False
    
    @property
    def rect(self):
        return pygame.Rect(
            (self.width, self.height),
            (ModeNode.WIDTH, ModeNode.HEIGHT),
        )

    def render(self):
        self.render_rect()
        self.render_text()

    def render_rect(self):
        fill_colour = ModeNode.BACKGROUND_COLOR
        if self.selected:
            fill_colour = ModeNode.BACKGROUND_COLOR_SELECTED
        pygame.draw.rect(SCREEN, fill_colour, self.rect, 0, ModeNode.BORDER_RADIUS)
        pygame.draw.rect(SCREEN, ModeNode.BORDER_COLOR, self.rect, 2, ModeNode.BORDER_RADIUS)

    def render_text(self):
        rect_surf = pygame.Surface((ModeNode.WIDTH-2, ModeNode.HEIGHT-2), pygame.SRCALPHA, 32)
        rect_surf = rect_surf.convert_alpha()

        surface = pygame.font.Font(None, 25).render(self.key, True, DARK_GREY)
        if len(self.key) > 11:
            rect_surf.blit(surface, (6, 15))
        elif len(self.key) > 10:
            rect_surf.blit(surface, (10, 15))
        else:
            rect_surf.blit(surface, (17, 15))

        SCREEN.blit(rect_surf, (self.width + 1, self.height + 1))
