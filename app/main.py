"""
TODO-LIST:
    - change the play and exit menu buttons to be hexagon shaped
    - highlighting for buttons
    - create label class
    - animate a cloud across the menu screen.
    - finish setting up players
    - fog of war
    - display time remaining in planning phase
    - add more songs to the music queue and add more music functionality
    - create buttons with images
    - apply button properties to unit icons
    - add button to take you back to main menu
    - move state constants to another file
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
            if event.type == self.music.song_end:
                print("song has ended")
                self.music.play_next_song()
            if event.type == pygame.QUIT:
                state = self.STATE_QUIT
            if state == self.STATE_MENU:
                state = self.menu.process_user_input(event)
            elif state == self.STATE_BOARD_GAME:
                state = self.game.process_user_input(event)


        return state

    def refresh(self, state):
        if state == self.STATE_MENU:
            self.menu.refresh()
        elif state == self.STATE_BOARD_GAME:
            self.game.refresh()

    def run(self):
        self.music.play_first_song()
        state = self.STATE_MENU
        while state != self.STATE_QUIT:
            state = self.process_user_input(state)
            self.refresh(state)
            pygame.display.flip()

if __name__ == '__main__':
    Main().run()
