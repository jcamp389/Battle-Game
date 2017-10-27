import pygame


pygame.init()
pygame.font.init()

LENGTH = 300
HEIGHT = 400
size = [LENGTH, HEIGHT]


black = (0, 0, 0)
lime_green = (22, 246, 74)
red = (255, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("BATTLE GAME")
running = 1


surface = pygame.Surface(screen.get_size())
#Rect(left, top, width, height) -> Rect
#300 / 400

#0,0                300,0
          #LOGO#


          #START#

          #QUIT#
#0,400              300,400

#Rect(left, top, width, height) -> Rect
exit_rect = pygame.Rect(LENGTH * .4, HEIGHT * .7, 80, 40)
play_rect = pygame.Rect(LENGTH * .4, HEIGHT * .3, 90, 50)
# #SysFont(name, size, bold=False, italic=False) -> Font
# exit_font = pygame.font.SysFont(None, 15, bold=True, italic=False)
#
# #rect(Surface, color, Rect, width=0) -> Rect
# # color = (255,255,255)
exit = pygame.draw.rect(surface, lime_green, exit_rect, 0)
play = pygame.draw.rect(surface, red, play_rect, 0)

# # #render(text, antialias, color, background=None)
exit_font = pygame.font.Font(None, 15, bold=True, italic=False)
exit_label = exit_font.render("EXIT GAME", True, white)
exit_textpos = exit_label.get_rect()
exit_textpos.centerx = exit_rect.get_rect().centerx

play_font = pygame.font.Font(None, 10, bold=True, italic=False)
play_label = exit_font.render("PLAY GAME", True, white)
play_textpos = play_label.get_rect()
play_textpos.centerx = play_rect.get_rect().centerx



while (running == 1):
    for event in pygame.event.get():

        if pygame.mouse.get_pressed()[0] == 1:
            my_mouse_pos = pygame.mouse.get_pos()
            my_mouse_pos_x = my_mouse_pos[0]
            my_mouse_pos_y = my_mouse_pos[1]

            if my_mouse_pos_x > exit_rect.left and \
               my_mouse_pos_x < exit_rect.right and \
               my_mouse_pos_y > exit_rect.top and \
               my_mouse_pos_y < exit_rect.bottom:
               running = 0

            elif my_mouse_pos_x > play_rect.left and \
               my_mouse_pos_x < play_rect.right and \
               my_mouse_pos_y > play_rect.top and \
               my_mouse_pos_y < play_rect.bottom:
                pass

#        , (exit_rect.centerx, exit_rect.centery))
#(play_rect.centerx, play_rect.centery))
        screen.blit(surface, (0, 0))
        screen.blit(exit_label)
        screen.blit(play_label)
        pygame.display.flip()