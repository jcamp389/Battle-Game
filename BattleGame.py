"""
TODO-LIST:
    - create background
    - connect ready button with phase text
    - highlighting for buttons
    - button enabled property
    - create label class
    - move the button click detection method into the button class.
    - add a turn timer (alternate between "plan" phase and "action" phase).
    - animate a cloud across the menu screen.
    - set up players (gets us into python classes).
    - set up home bases.
"""


import pygame
import random
import threading

pygame.init()
pygame.font.init()
pygame.mixer.init()


STATE_MENU = 0
STATE_QUIT = 1
STATE_BOARD_GAME = 2


SCREENLENGTH = 1000
SCREENHEIGHT = 600
BOARDHEIGHT = SCREENHEIGHT * .8
BOARDLENGTH = SCREENLENGTH * .8
size = [SCREENLENGTH, SCREENHEIGHT]


music_is_playing = True

current_phase = "PLANNING PHASE"


def load_music():
    try:
        intro_screen_music = pygame.mixer.music.load('Pippin.mp3')
        pygame.mixer.music.play(-1)
    except Exception as exc:
        print("Exception loading music: {}".format(exc))


intro_screen_background = pygame.image.load('Intro_Screen_Background.jpg')
intro_screen_background = pygame.transform.scale(intro_screen_background, (SCREENLENGTH, SCREENHEIGHT))

unit_scale_factor = int((BOARDHEIGHT/10) * .8)
bow = pygame.image.load('bow.png')
bow = pygame.transform.scale(bow, (unit_scale_factor, unit_scale_factor))
sword = pygame.image.load('sword.png')
sword = pygame.transform.scale(sword, (unit_scale_factor, unit_scale_factor))
spear = pygame.image.load('spear.png')
spear = pygame.transform.scale(spear, (unit_scale_factor, unit_scale_factor))
horseman = pygame.image.load('horseman1.png')
horseman = pygame.transform.scale(horseman, (unit_scale_factor, unit_scale_factor))

# colors
black = (0, 0, 0)
lime_green = (22, 246, 74)
yellow = (255, 255, 0)
brown = (165, 42, 42)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
grey = (64, 64, 64)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("HEXCELSIOR")

surface = pygame.Surface(screen.get_size())

board_offset = (25, 25)


class Button(pygame.sprite.Sprite):
    def __init__(self, title, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)

        self.title = title
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True

    def __repr__(self):
        return "{} ({}, {})".format(self.title, self.x, self.y)

    def draw(self, surface):
        if self.visible is False:
            return
        print(self.visible)
        rect = pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, self.width, self.height), 2)
        font = pygame.font.Font(None, 15, bold=True, italic=False)
        label = font.render(self.title, True, self.color)
        label_pos = label.get_rect()
        label_pos.centerx = rect.centerx
        label_pos.centery = rect.centery
        screen.blit(label, label_pos)


    def is_clicked(self, x=None, y=None):
        if x is None or y is None:
            my_mouse_pos = pygame.mouse.get_pos()
            x = my_mouse_pos[0]
            y = my_mouse_pos[1]

        if self.rect.left < x < self.rect.right and self.rect.top < y < self.rect.bottom:
            return True
        return False

    def set_visibility(self, visible=True):
        self.visible = visible

class BoardTile(pygame.sprite.Sprite):
    def __init__(self, top_right, top_left, left, bot_left, bot_right, right, tile_color):
        pygame.sprite.Sprite.__init__(self)

        self.top_left = top_left
        self.top_right = top_right
        self.right = right
        self.bot_right = bot_right
        self.bot_left = bot_left
        self.left = left
        self.tile_color = tile_color
        self.rect = pygame.Rect(top_left[0], top_left[1], top_right[0] - top_left[0], bot_left[1] - top_left[1])

    def get_tile_coordinates(self):
        return self.top_left, self.top_right, self.right, self.bot_right, self.bot_left, self.left

    def contains(self, x, y):
        # adapted from http://www.ariel.com.au/a/python-point-int-poly.html
        coordinates = self.get_tile_coordinates()
        n = len(coordinates)
        contains_point = False

        p1x, p1y = coordinates[0]
        for i in range(n + 1):
            p2x, p2y = coordinates[i % n]
            if y > min(p1y, p2y) and y <= max(p1y, p2y) and x <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (y-p1y) * (p2x-p1x) / (p2y-p1y) + p1x
                if p1x == p2x or x <= xinters:
                    contains_point = not contains_point
            p1x, p1y = p2x, p2y

        return contains_point

    def __repr__(self):
        return "{} {} {} {} {} {}".format(self.top_left, self.top_right, self.right, self.bot_right, self.bot_left, self.left)

exit_button = Button("EXIT GAME", SCREENLENGTH * .45, SCREENHEIGHT * .3, 80, 40, white)
play_button = Button("PLAY GAME", SCREENLENGTH * .45, SCREENHEIGHT * .2, 80, 40, white)
toggle_music_button = Button("TOGGLE MUSIC", SCREENLENGTH * .9, 0, 100, 40, white)
ready_button = Button("READY", SCREENLENGTH * .6, SCREENHEIGHT * .01, 100, 40, white)


board = None


def display_xy():
    font = pygame.font.Font(None, 15, bold=True, italic=False)

    current_mouse_pos = pygame.mouse.get_pos()
    current_xy_text_list = ["x: ", str(current_mouse_pos[0]), "y: ", str(current_mouse_pos[1])]
    final_xy_list = " ".join(current_xy_text_list)
    currentxy_label = font.render(str(final_xy_list), True, red)
    currentxy_labelpos = currentxy_label.get_rect()
    currentxyrect = pygame.Rect(SCREENLENGTH * .8, SCREENHEIGHT * .01, 80, 15)
    currentxy_labelpos.centerx = currentxyrect.centerx
    currentxy_labelpos.centery = currentxyrect.centery
    screen.blit(currentxy_label, (currentxy_labelpos.centerx - 35, currentxy_labelpos.centery - 5))

def display_phase():
    global current_phase
    font = pygame.font.Font(None, 15, bold=True, italic=False)
    phase_label = font.render(current_phase, True, red)
    phase_labelpos = phase_label.get_rect()
    phase_rect = pygame.Rect(SCREENLENGTH * .35, SCREENHEIGHT * .01, 80, 15)
    phase_labelpos.centerx = phase_rect.centerx
    phase_labelpos.centery = phase_rect.centery
    screen.blit(phase_label, (phase_labelpos.centerx - 35, phase_labelpos.centery - 5))

def changephase():
    global current_phase
    timer = threading.Timer(30.0, changephase)
    timer.daemon = True
    timer.start()
    if current_phase == "PLANNING PHASE":
        current_phase = "ACTION PHASE"
    else:
        current_phase = "PLANNING PHASE"

def action_sequence():
    global ready_button
    ready_button.set_visibility(visible=False)




def display_toggle_music(surface):
    toggle_music_button.draw(surface)


def menu_screen_refresh():
    screen.blit(intro_screen_background, (0, 0))
    exit_button.draw(intro_screen_background)
    play_button.draw(intro_screen_background)
    display_xy()
    display_toggle_music(intro_screen_background)

def game_screen_refresh():
    screen.blit(surface, (0, 0))
    screen.blit(bow, (830,115))
    screen.blit(sword, (870, 115))
    screen.blit(spear, (910,115))
    screen.blit(horseman, (950, 115))
    ready_button.draw(surface)
    board_game()



def random_tile():
    possible_tiles = [red, white, green, brown, yellow]
    index = random.randint(0, len(possible_tiles) - 1)
    return possible_tiles[index]


def board_initializer():
    count_per_column = 10
    count_per_row = count_per_column * 2
    dimensions = BOARDHEIGHT / count_per_column
    board_matrix = []
    for i in range(0, count_per_row):
        board_matrix.append([])
        for j in range(0, count_per_column):
            is_row_even = i % 2 == 0
            x = j * (dimensions * 1.5)
            if not is_row_even:
                x += (dimensions * .75)
            y = i * (dimensions * .425)
            y += dimensions/2

            # Account for the board not starting in the exact top-left corner of the screen.
            x += board_offset[0]
            y += board_offset[1]

            h = BoardTile((x + (dimensions * .75), y + (dimensions * .075)),
                (x + (dimensions * .25), y + (dimensions * .075)),
                (x, y + (dimensions * .5)),
                (x + (dimensions * .25), y + (dimensions * .925)),
                (x + (dimensions * .75), y + (dimensions * .925)),
                (x + dimensions, y + (dimensions * .5)), random_tile())
            board_matrix[i].append(h)

    return board_matrix


def is_mouse_in_coordinates(tile, mouse_x, mouse_y):
    # returns True if mouse x and mosue y inside this BoardTile, else False
    if tile.contains(mouse_x, mouse_y):
        return True
    else:
        return False


def board_game():
    global board
    currently_highlighted_tile = None
    if board is None:
        changephase()
        board = board_initializer()
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            current_tile = board[i][j]
            if is_mouse_in_coordinates(current_tile, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                currently_highlighted_tile = current_tile
            draw_color = grey if current_tile == currently_highlighted_tile else current_tile.tile_color
            pygame.draw.polygon(surface, draw_color, current_tile.get_tile_coordinates(), 0)
            # border pass
            pygame.draw.polygon(surface, grey, current_tile.get_tile_coordinates(), 2)


    display_xy()
    display_phase()
    display_toggle_music(surface)





def toggle_music():
    global music_is_playing
    music = pygame.mixer.music
    if music_is_playing:
        music.pause()
        music_is_playing = False
    else:
        music.unpause()
        music_is_playing = True


def process_user_input(state):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = STATE_QUIT

        elif state == STATE_MENU:
            if pygame.mouse.get_pressed()[0] == 1:
                my_mouse_pos = pygame.mouse.get_pos()
                if exit_button.is_clicked(my_mouse_pos[0], my_mouse_pos[1]):
                    state = STATE_QUIT
                elif play_button.is_clicked(my_mouse_pos[0], my_mouse_pos[1]):
                    state = STATE_BOARD_GAME
                elif toggle_music_button.is_clicked(my_mouse_pos[0], my_mouse_pos[1]):
                    toggle_music()
            menu_screen_refresh()

        elif state == STATE_BOARD_GAME:
            if pygame.mouse.get_pressed()[0] == 1:
                my_mouse_pos = pygame.mouse.get_pos()
                if toggle_music_button.is_clicked(my_mouse_pos[0], my_mouse_pos[1]):
                    toggle_music()
                elif ready_button.is_clicked():
                    action_sequence()


    return state


load_music()


state = STATE_MENU
has_drawn_board = False
while state != STATE_QUIT:
    if state == STATE_BOARD_GAME:
        game_screen_refresh()
    state = process_user_input(state)
    pygame.display.flip()
