from app.properties import Properties as Props
from app.sprites import BoardTile, Button
import random
import pygame
import threading
from app.utils import Utils

class Game(object):
    def __init__(self, screen, surface, music):
        self.STATE_QUIT = 1
        self.STATE_BOARD_GAME = 2
        self.music = music
        self.screen = screen
        self.surface = surface
        self.board = None
        self.board_offset = (25, 25)
        self.current_phase = 'PLANNING PHASE'

        self.BOARDHEIGHT = Props.SCREENHEIGHT * .8
        self.BOARDLENGTH = Props.SCREENLENGTH * .8
        self.ready_button = Button("READY", Props.SCREENLENGTH * .6, Props.SCREENHEIGHT * .01, 100, 40, Props.white)

        unit_scale_factor = int((self.BOARDHEIGHT/10) * .8)
        bow = pygame.image.load('images/bow.png')
        self.bow = pygame.transform.scale(bow, (unit_scale_factor, unit_scale_factor))
        sword = pygame.image.load('images/sword.png')
        self.sword = pygame.transform.scale(sword, (unit_scale_factor, unit_scale_factor))
        spear = pygame.image.load('images/spear.png')
        self.spear = pygame.transform.scale(spear, (unit_scale_factor, unit_scale_factor))
        horseman = pygame.image.load('images/horseman1.png')
        self.horseman = pygame.transform.scale(horseman, (unit_scale_factor, unit_scale_factor))

    def board_initializer(self):
        count_per_column = 10
        count_per_row = count_per_column * 2
        dimensions = self.BOARDHEIGHT / count_per_column
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
                x += self.board_offset[0]
                y += self.board_offset[1]

                h = BoardTile((x + (dimensions * .75), y + (dimensions * .075)),
                    (x + (dimensions * .25), y + (dimensions * .075)),
                    (x, y + (dimensions * .5)),
                    (x + (dimensions * .25), y + (dimensions * .925)),
                    (x + (dimensions * .75), y + (dimensions * .925)),
                    (x + dimensions, y + (dimensions * .5)), self.random_tile())
                board_matrix[i].append(h)
        return board_matrix

    def random_tile(self):
        possible_tiles = [Props.red, Props.white, Props.green, Props.brown, Props.yellow]
        index = random.randint(0, len(possible_tiles) - 1)
        return possible_tiles[index]

    def refresh(self):
        self.screen.blit(self.surface, (0, 0))
        self.screen.blit(self.bow, (830,115))
        self.screen.blit(self.sword, (870, 115))
        self.screen.blit(self.spear, (910,115))
        self.screen.blit(self.horseman, (950, 115))
        self.ready_button.draw(self.surface, self.screen)
        self.board_game()
        self.display_phase()
        Utils.display_xy(self.screen)
        self.music.music_button.draw(self.surface, self.screen)

    def display_phase(self):
        font = pygame.font.Font(None, 15, bold=True, italic=False)
        phase_label = font.render(self.current_phase, True, Props.red)
        phase_labelpos = phase_label.get_rect()
        phase_rect = pygame.Rect(Props.SCREENLENGTH * .35, Props.SCREENHEIGHT * .01, 80, 15)
        phase_labelpos.centerx = phase_rect.centerx
        phase_labelpos.centery = phase_rect.centery
        self.screen.blit(phase_label, (phase_labelpos.centerx - 35, phase_labelpos.centery - 5))

    def changephase(self):
        timer = threading.Timer(30.0, self.changephase)
        timer.daemon = True
        timer.start()
        if self.current_phase == "PLANNING PHASE":
            self.current_phase = "ACTION PHASE"
        else:
            self.current_phase = "PLANNING PHASE"

    def action_sequence(self):
        self.ready_button.set_visibility(visible=False)

    def board_game(self):
        currently_highlighted_tile = None
        if self.board is None:
            self.changephase()
            self.board = self.board_initializer()
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[0])):
                current_tile = self.board[i][j]
                if current_tile.contains(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    currently_highlighted_tile = current_tile
                draw_color = Props.grey if current_tile == currently_highlighted_tile else current_tile.tile_color
                pygame.draw.polygon(self.surface, draw_color, current_tile.get_tile_coordinates(), 0)
                # border pass
                pygame.draw.polygon(self.surface, Props.grey, current_tile.get_tile_coordinates(), 2)

    def process_user_input(self):
        state = self.STATE_BOARD_GAME
        if self.music.music_button.is_clicked():
            self.music.toggle_music()
        elif self.ready_button.is_clicked():
            self.action_sequence()
        self.refresh()
        return state