import pygame
from app.properties import Properties as Props
from app.sprites import Button
from app.utils import Utils


class Menu(object):
    def __init__(self, screen, surface, music):
        self.STATE_MENU = 0
        self.STATE_QUIT = 1
        self.STATE_BOARD_GAME = 2

        self.screen = screen
        self.surface = surface
        self.music = music



        intro_screen_background = pygame.image.load('images/Intro_Screen_Background.jpg')
        self.intro_screen_background = pygame.transform.scale(intro_screen_background, (Props.SCREENLENGTH, Props.SCREENHEIGHT))

        self.title = pygame.image.load("images/Hexcelsior.png")

        self.exit_button = Button("EXIT GAME", Props.SCREENLENGTH * .45, Props.SCREENHEIGHT * .3, 80, 40, Props.white)
        self.play_button = Button("PLAY GAME", Props.SCREENLENGTH * .45, Props.SCREENHEIGHT * .2, 80, 40, Props.white)

    def display_toggle_music(self, surface, screen):
        self.toggle_music_button.draw(surface, screen)

    def refresh(self):
        self.screen.blit(self.intro_screen_background, (0, 0))
        self.screen.blit(self.title, (Props.SCREENLENGTH * .22, Props.SCREENHEIGHT * .05))
        self.exit_button.draw(self.screen)
        self.play_button.draw(self.screen)
        Utils.display_xy(self.screen)
        self.music.music_button.draw(self.screen)

    def process_user_input(self, event):
        state = self.STATE_MENU
        if pygame.mouse.get_pressed()[0] == 1:
            if self.exit_button.is_clicked(event):
                state = self.STATE_QUIT
            elif self.play_button.is_clicked(event):
                state = self.STATE_BOARD_GAME
            elif self.music.music_button.is_clicked(event):
                self.music.toggle_music()
        return state
