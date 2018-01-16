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
from app.properties import Properties as Props
from app.menu import Menu
from app.game import Game
from app.music import Music


class Main(object):
    def __init__(self):
        self.STATE_MENU = 0
        self.STATE_QUIT = 1
        self.STATE_BOARD_GAME = 2
        self.current_phase = "PLANNING PHASE"
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(Props.size)
        self.surface = pygame.Surface(self.screen.get_size())
        pygame.display.set_caption("HEXCELSIOR")

        # Our menu and game screens
        self.music = Music()
        self.menu = Menu(self.screen, self.surface, self.music)
        self.game = Game(self.screen, self.surface, self.music)

    def process_user_input(self, state):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = self.STATE_QUIT
            elif state == self.STATE_MENU:
                state = self.menu.process_user_input()
            elif state == self.STATE_BOARD_GAME:
                state = self.game.process_user_input()
        return state

    def run(self):
        self.music.load_music()
        state = self.STATE_MENU
        while state != self.STATE_QUIT:
            state = self.process_user_input(state)
            pygame.display.flip()

if __name__ == '__main__':
    Main().run()