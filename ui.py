# Import and initialize the pygame library
import pygame
import Keys

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

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_RETURN
)

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

# def main():
#     keys = []
#     user_input = ""

user_input = "Hello world"
running = True
alpha = True
upper = False
cursor = KEYS.root

while running:

    # logic part
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # move the cursor
        if event.type == K_LEFT:
            if cursor.is_leaf():
                cursor = KEYS.root
            else:
                cursor = cursor.left

        if event.type == K_RIGHT:
            if cursor.is_leaf():
                cursor = KEYS.root
            else:
                cursor = cursor.right

        if event.type == K_RETURN:
            key = ""
            if alpha:
                key = cursor.alpha_key
            else:
                key = cursor.punc_key

            if len(key) == 1:
                user_input += key
            elif key == "Space":
                user_input += " "
            elif key == "Delete":
                user_input = user_input[:-1]
            elif key == "Clear":
                user_input = ""
            elif key == "Upper":
                upper = not upper
            elif key == "123":
                alpha = False
            elif key == "abc":
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

        # fill the current cursor with light grey

        # cursor_rect = pygame.Rect((cursor.width+1, cursor.height+1), (RECT_X-2, RECT_Y-2))
        # pygame.draw.rect(SCREEN, LIGHT_GREY, cursor_rect)
        # print("rect")

        cursor_surf = pygame.Surface((RECT_X-2, RECT_Y-2))
        cursor_surf.fill(LIGHT_GREY)
        SCREEN.blit(cursor_surf, (cursor.width+1, cursor.height+1))

        # option or key
        if alpha:
            if len(tmp.alpha_key) > 1:
                surface = OPTION_FONT.render(tmp.alpha_key, True, DARK_GREY)
                if len(tmp.alpha_key) == 5:
                    SCREEN.blit(surface, (tmp.width + 3, tmp.height + 10))
                elif len(tmp.alpha_key) == 3:
                    SCREEN.blit(surface, (tmp.width + 10, tmp.height + 10))
                else:
                    SCREEN.blit(surface, (tmp.width + 1, tmp.height + 10))
            else:
                if cursor.width == tmp.width and cursor.height == tmp.height:
                    surface = KEY_FONT.render(tmp.alpha_key, True, DARK_GREY)
                    cursor_surf.blit(surface, (18, 6))
                    print("alpha1")
                else:
                    surface = KEY_FONT.render(tmp.alpha_key, True, DARK_GREY)
                    SCREEN.blit(surface, (tmp.width + 18, tmp.height + 6))
                    print("alpha2")
        else:
            if len(str(tmp.punc_key)) > 1:
                surface = OPTION_FONT.render(tmp.punc_key, True, DARK_GREY)
                if len(tmp.alpha_key) == 5:
                    SCREEN.blit(surface, (tmp.width + 3, tmp.height + 10))
                elif len(tmp.alpha_key) == 3:
                    SCREEN.blit(surface, (tmp.width + 10, tmp.height + 10))
                else:
                    SCREEN.blit(surface, (tmp.width + 1, tmp.height + 10))
            else:
                surface = KEY_FONT.render(str(tmp.punc_key), True, DARK_GREY)
                SCREEN.blit(surface, (tmp.width + 18, tmp.height + 6))

        j += 1
        if j >= len(LAYER_WIDTH[i]):
            i += 1
            j = 0

    # Flip the display
    pygame.display.flip()
    clock = pygame.time.Clock()
    clock.tick(1)


# Done! Time to quit.
pygame.quit()

# if __name__ == "__main__":
#     main()