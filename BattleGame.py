import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()
pygame.mixer.init()

LENGTH = 600
HEIGHT = 600
size = [LENGTH, HEIGHT]

intro_screen_background = pygame.image.load('Intro_Screen_Background.jpg')
intro_screen_music = pygame.mixer.music.load('Pippin.mp3')

black = (0, 0, 0)
lime_green = (22, 246, 74)
red = (255, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("BATTLE GAME")
running = 1

surface = pygame.Surface(screen.get_size())
board_surface = pygame.Surface((LENGTH * .80, HEIGHT * .80))


# Rect(left, top, width, height) -> Rect
# 300 / 400

# 0,0                300,0
# LOGO#


# START#

# QUIT#
# 0,400              300,400

# Rect(left, top, width, height) -> Rect
exit_rect = pygame.Rect(LENGTH * .45, HEIGHT * .3, 80, 40)
play_rect = pygame.Rect(LENGTH * .45, HEIGHT * .2, 80, 40)
# #SysFont(name, size, bold=False, italic=False) -> Font
# exit_font = pygame.font.SysFont(None, 15, bold=True, italic=False)
#
# #rect(Surface, color, Rect, width=0) -> Rect
# # color = (255,255,255)
exit = pygame.draw.rect(intro_screen_background, white, exit_rect, 2)
play = pygame.draw.rect(intro_screen_background, white, play_rect, 2)

# # #render(text, antialias, color, background=None)
exit_font = pygame.font.Font(None, 15, bold=True, italic=False)
exit_label = exit_font.render("EXIT GAME", True, white)
exit_labelpos = exit_label.get_rect()
exit_labelpos.centerx = exit.centerx
exit_labelpos.centery = exit.centery

play_font = pygame.font.Font(None, 10, bold=True, italic=False)
play_label = exit_font.render("PLAY GAME", True, white)
play_labelpos = play_label.get_rect()
play_labelpos.centerx = play.centerx
play_labelpos.centery = play.centery


#
#
#
#
#

# pygame.Rect(i * 20, j * 20, 20, 20)
# index of the columns should map to an x value
# index of the row should map to a y value
# 20x20
#
#     0,0 20,0      20,0 40,0
#     []             []            [][][][]
#     0,20 20,20
#     []       [][][][][]
#
#















def menu_screen_refresh():
    screen.blit(intro_screen_background, (0, 0))
    screen.blit(exit_label, (exit_labelpos.centerx - 30, exit_labelpos.centery))
    screen.blit(play_label, (play_labelpos.centerx - 30, play_labelpos.centery))
    pygame.display.flip()


def board_game(event):
    for i in range(0, 20):
        for j in range(0, 20):
            new_rect = pygame.Rect(i * 20, j * 20, 20, 20)
            draw_new_rect = pygame.draw.rect(board_surface, red, new_rect, 1)
    screen.blit(surface, (0, 0))
    screen.blit(board_surface, (30, 30))
    pygame.display.flip()


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

pygame.mixer.music.play(-1)
# 0 = menu
# 1 = quit
# 2 = leaderboard
# 3 = board game
state = 0
while (state != 1):
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
        elif state == 3:
            board_game(event)
