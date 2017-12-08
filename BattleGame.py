"""

TODO-LIST:
    - replace the `state` ints with a set of constants (like an enum).
    - have the tiles highlight when you hover.
    - set up players (gets us into python classes).
    - animate a cloud across the menu screen.
    - set up home bases.

"""


import pygame
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

LENGTH = 1000
HEIGHT = 600
size = [LENGTH, HEIGHT]


def load_music():
    try:
        intro_screen_music = pygame.mixer.music.load('Pippin.mp3')
        pygame.mixer.music.play(-1)
    except Exception as exc:
        print("Exception loading music: {}".format(exc))


intro_screen_background = pygame.image.load('Intro_Screen_Background.jpg')
intro_screen_background = pygame.transform.scale(intro_screen_background, (LENGTH, HEIGHT))

# colors
black = (0, 0, 0)
lime_green = (22, 246, 74)
yellow = (255, 255, 0)
brown = (165, 42, 42)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
grey = (244, 246, 249)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("HEXCELSIOR")

surface = pygame.Surface(screen.get_size())
board_surface = pygame.Surface(screen.get_size())

exit_rect = pygame.Rect(LENGTH * .45, HEIGHT * .3, 80, 40)
play_rect = pygame.Rect(LENGTH * .45, HEIGHT * .2, 80, 40)

exit = pygame.draw.rect(intro_screen_background, white, exit_rect, 2)
play = pygame.draw.rect(intro_screen_background, white, play_rect, 2)

exit_font = pygame.font.Font(None, 15, bold=True, italic=False)
exit_label = exit_font.render("EXIT GAME", True, white)
exit_labelpos = exit_label.get_rect()
exit_labelpos.centerx = exit.centerx
exit_labelpos.centery = exit.centery

play_font = pygame.font.Font(None, 15, bold=True, italic=False)
play_label = play_font.render("PLAY GAME", True, white)
play_labelpos = play_label.get_rect()
play_labelpos.centerx = play.centerx
play_labelpos.centery = play.centery

board = None

def display_xy():
    current_mouse_pos = pygame.mouse.get_pos()
    current_xy_text_list = ["x: ", str(current_mouse_pos[0]), "y: ", str(current_mouse_pos[1])]
    final_xy_list = " ".join(current_xy_text_list)
    currentxy_label = exit_font.render(str(final_xy_list), True, red)
    currentxy_labelpos = play_label.get_rect()
    currentxyrect = pygame.Rect(LENGTH * .8, HEIGHT * .01, 80, 15)
    currentxy = pygame.draw.rect(intro_screen_background, red, currentxyrect, 2)
    currentxy_labelpos.centerx = currentxy.centerx
    currentxy_labelpos.centery = currentxy.centery
    screen.blit(currentxy_label, (currentxy_labelpos.centerx - 35, currentxy_labelpos.centery - 5))

def menu_screen_refresh():
    screen.blit(intro_screen_background, (0, 0))
    screen.blit(exit_label, (exit_labelpos.centerx - 30, exit_labelpos.centery))
    screen.blit(play_label, (play_labelpos.centerx - 30, play_labelpos.centery))
    display_xy()

class Hexagon(object):
    def __init__(self, top_left, top_right, right, bot_right, bot_left, left, tile_color):
        self.top_left = top_left
        self.top_right = top_right
        self.right = right
        self.bot_right = bot_right
        self.bot_left = bot_left
        self.left = left
        self.tile_color = tile_color

    def __repr__(self):
        return "{} {} {} {} {} {}".format(self.top_left, self.top_right, self.right, self.bot_right, self.bot_left, self.left)

def board_initializer():
    count_per_column = 10
    count_per_row = count_per_column * 2
    dimensions = HEIGHT / count_per_column
    board_matrix = []
    for i in range(0, count_per_row):
        board_matrix.append([])
        for j in range(0, count_per_column):
            is_row_even = i % 2 == 0
            x = j * (dimensions * 1.5)
            if not is_row_even:
                x += (dimensions * .75)
            y = i * (dimensions * .425)

            h = Hexagon((x + (dimensions * .75), y + (dimensions * .075)),
                (x + (dimensions * .25), y + (dimensions * .075)),
                (x, y + (dimensions * .5)),
                (x + (dimensions * .25), y + (dimensions * .925)),
                (x + (dimensions * .75), y + (dimensions * .925)),
                (x + dimensions, y + (dimensions * .5)), random_tile())
            board_matrix[i].append(h)

    return board_matrix

def is_mouse_in_coordinates(tile, mouse_x, mouse_y):
    # returns True if mouse x and mosue y inside this hexagon, else False
    tl = tile.top_left
    return False

def board_game():
    global board
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            current_tile = board[i][j]
            if is_mouse_in_coordinates(current_tile, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                current_tile.tile_color = grey
            pygame.draw.polygon(board_surface, current_tile.tile_color,
                                (current_tile.top_left, current_tile.top_right, current_tile.right, current_tile.bot_right, current_tile.bot_left, current_tile.left), 0)
            # border pass
            pygame.draw.polygon(board_surface, grey,
                                (current_tile.top_left, current_tile.top_right, current_tile.right, current_tile.bot_right, current_tile.bot_left, current_tile.left), 2)

    screen.blit(surface, (0, 0))
    screen.blit(board_surface, (25, 25))
    display_xy()


def random_tile():
    possible_tiles = [red, white, green, brown, yellow]
    index = random.randint(0, len(possible_tiles) - 1)
    return possible_tiles[index]


def quit_button_clicked(x, y):
    if x > exit_rect.left and \
                    x < exit_rect.right and \
                    y > exit_rect.top and \
                    y < exit_rect.bottom:
        return True
    return False

def start_button_clicked(x, y):
    if x > play_rect.left and \
                    x < play_rect.right and \
                    y > play_rect.top and \
                    y < play_rect.bottom:
        return True
    return False

def process_user_input(state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = 1
        if state == 0:
            if pygame.mouse.get_pressed()[0] == 1:
                my_mouse_pos = pygame.mouse.get_pos()
                if quit_button_clicked(my_mouse_pos[0], my_mouse_pos[1]):
                    state = 1
                elif start_button_clicked(my_mouse_pos[0], my_mouse_pos[1]):
                    state = 3

            menu_screen_refresh()


    return state


def draw_current_state_of_board(state, has_drawn_board):
    if state != 3:
        # we're in the wrong state. return early, and say we didn't draw the board.
        return False
    
    global board
    if board is not None:
        # we've already drawn the board. return early, and report that we have drawn the board.
        return True

    # everything is chill. let's draw the board and then report that we drew it.
    board = board_initializer()
    return True


load_music()

# 0 = menu
# 1 = quit
# 2 = leaderboard
# 3 = board game
state = 0
has_drawn_board = False
while state != 1:
    if has_drawn_board: board_game()
    state = process_user_input(state)
    has_drawn_board = draw_current_state_of_board(state, has_drawn_board)
    pygame.display.flip()

