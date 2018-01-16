import pygame
from app.properties import Properties as Props


class Utils(object):
    @staticmethod
    def display_xy(screen):
        font = pygame.font.Font(None, 15, bold=True, italic=False)
        current_mouse_pos = pygame.mouse.get_pos()
        current_xy_text_list = ["x: ", str(current_mouse_pos[0]), "y: ", str(current_mouse_pos[1])]
        final_xy_list = " ".join(current_xy_text_list)
        currentxy_label = font.render(str(final_xy_list), True, Props.red)
        currentxy_labelpos = currentxy_label.get_rect()
        currentxyrect = pygame.Rect(Props.SCREENLENGTH * .8, Props.SCREENHEIGHT * .01, 80, 15)
        currentxy_labelpos.centerx = currentxyrect.centerx
        currentxy_labelpos.centery = currentxyrect.centery
        screen.blit(currentxy_label, (currentxy_labelpos.centerx - 35, currentxy_labelpos.centery - 5))
