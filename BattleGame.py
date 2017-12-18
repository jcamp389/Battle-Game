"""
TODO-LIST:
    - replace the `state` ints with a set of constants (like an enum).
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
grey = (64, 64, 64)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("HEXCELSIOR")

surface = pygame.Surface(screen.get_size())

board_offset = (25, 25)

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


def random_tile():
    possible_tiles = [red, white, green, brown, yellow]
    index = random.randint(0, len(possible_tiles) - 1)
    return possible_tiles[index]


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

    screen.blit(surface, (0, 0))
    display_xy()


def quit_button_clicked(x, y):
    if exit_rect.left < x < exit_rect.right and exit_rect.top < y < exit_rect.bottom:
        return True
    return False


def start_button_clicked(x, y):
    if play_rect.left < x < play_rect.right and play_rect.top < y < play_rect.bottom:
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


load_music()


# 0 = menu
# 1 = quit
# 2 = leaderboard
# 3 = board game
state = 0
has_drawn_board = False
while state != 1:
    if state == 3:
        board_game()
    state = process_user_input(state)
    pygame.display.flip()
