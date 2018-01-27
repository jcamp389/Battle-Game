from app.properties import Properties as Props
from app.sprites import BoardTile, Button
import random
import pygame
import threading
from app.utils import Utils

class Player(object):
    def __init__(self, name, number, color, base_tile):
        self.name = name
        self.number = number
        self.color = color
        self.base_tile = base_tile
        self.cost = 4
        self.units = []

class Game(object):
    def __init__(self, screen, surface, music):
        self.STATE_MENU = 0
        self.STATE_QUIT = 1
        self.STATE_BOARD_GAME = 2
        self.music = music
        self.screen = screen
        self.surface = surface
        self.board = None
        self.board_offset = (25, 25)

        self.back_button = Button("Home Screen", Props.SCREENLENGTH * 0, Props.SCREENHEIGHT * 0, 80, 40, Props.white)

        self.background = pygame.image.load('images/old_paper.png')
        self.background = pygame.transform.scale(self.background, (Props.SCREENLENGTH, Props.SCREENHEIGHT))
        self.PHASE_PLANNING = 1
        self.PHASE_ACTION = 2
        self.current_phase = self.PHASE_PLANNING

        self.BOARDHEIGHT = Props.SCREENHEIGHT * .8
        self.BOARDLENGTH = Props.SCREENLENGTH * .8
        self.ready_button = Button("READY", Props.SCREENLENGTH * .6, Props.SCREENHEIGHT * 0, 100, 40, Props.white)

        unit_scale_factor = int((self.BOARDHEIGHT/10) * .8)
        bow = pygame.image.load('images/bow.png')
        self.bow = pygame.transform.scale(bow, (unit_scale_factor, unit_scale_factor))
        sword = pygame.image.load('images/sword.png')
        self.sword = pygame.transform.scale(sword, (unit_scale_factor, unit_scale_factor))
        spear = pygame.image.load('images/spear.png')
        self.spear = pygame.transform.scale(spear, (unit_scale_factor, unit_scale_factor))
        horseman = pygame.image.load('images/horseman1.png')
        self.horseman = pygame.transform.scale(horseman, (unit_scale_factor, unit_scale_factor))

        self.changephase(should_change_phase=False)
        self.board = self.board_initializer()

        #we are manually going to create players for now
        player_1 = Player(name="Joel", number=1, color=Props.black, base_tile=self.board[4][5])
        player_2 = Player(name="John", number=2, color=Props.green, base_tile=self.board[15][2])
        player_3 = Player(name="Michael", number=3, color=Props.red, base_tile=self.board[15][7])
        self.players = [player_1, player_2, player_3]


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
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.bow, (830,115))
        self.screen.blit(self.sword, (870, 115))
        self.screen.blit(self.spear, (910,115))
        self.screen.blit(self.horseman, (950, 115))
        self.ready_button.draw(self.screen)
        self.back_button.draw(self.screen)
        self.board_game()
        self.display_phase()
        Utils.display_xy(self.screen)
        self.music.music_button.draw(self.screen)

        if self.current_phase == self.PHASE_PLANNING:
            self.ready_button.set_visibility(visible=True)
            self.ready_button.set_enabled(enabled=True)
        else:
            self.ready_button.set_visibility(visible=False)
            self.ready_button.set_enabled(enabled=False)


    def display_phase(self):
        font = pygame.font.Font(None, 15, bold=True, italic=False)
        phase_title = "PLANNING PHASE" if self.current_phase == self.PHASE_PLANNING else "ACTION PHASE"
        phase_label = font.render(phase_title, True, Props.red)
        phase_labelpos = phase_label.get_rect()
        phase_rect = pygame.Rect(Props.SCREENLENGTH * .35, Props.SCREENHEIGHT * .01, 80, 15)
        phase_labelpos.centerx = phase_rect.centerx
        phase_labelpos.centery = phase_rect.centery
        self.screen.blit(phase_label, (phase_labelpos.centerx - 35, phase_labelpos.centery - 5))

    def changephase(self, should_change_phase=True):
        self.timer = threading.Timer(5.0, self.changephase)
        self.timer.daemon = True
        self.timer.start()
        if should_change_phase == False:
            return
        if self.current_phase == self.PHASE_PLANNING:
            self.current_phase = self.PHASE_ACTION
        else:
            self.current_phase = self.PHASE_PLANNING

    def board_game(self):
        currently_highlighted_tile = None
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[0])):
                current_tile = self.board[i][j]
                if current_tile.contains(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    currently_highlighted_tile = current_tile
                draw_color = Props.grey if current_tile == currently_highlighted_tile else current_tile.tile_color
                if i == 4 and j == 5:
                    draw_color = Props.black
                if i == 15 and j == 2:
                    draw_color = Props.black
                elif i == 15 and j == 7:
                    draw_color = Props.black

                pygame.draw.polygon(self.background, draw_color, current_tile.get_tile_coordinates(), 0)
                # border pass
                pygame.draw.polygon(self.background, Props.grey, current_tile.get_tile_coordinates(), 2)

    def process_user_input(self, event):
        state = self.STATE_BOARD_GAME
        if self.music.music_button.is_clicked(event):
            self.music.toggle_music()
        elif self.ready_button.is_clicked(event):
            self.timer.cancel()
            self.changephase()
        elif self.back_button.is_clicked(event):
            state = self.STATE_MENU
        return state
