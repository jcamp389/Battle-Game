
#songs = {'sounds/Thatched Villagers.mp3', 'sounds/Mountain Emperor.mp3', 'sounds/Moorland.mp3',
#                    'sounds/Hidden Past.mp3', 'sounds/Galway.mp3', 'sounds/Angevin B.mp3'}

from app.sprites import Button
from app.properties import Properties as Props
import pygame


class Music(object):
    def __init__(self):
        self.music_button = Button("TOGGLE MUSIC", Props.SCREENLENGTH * .9, 0, 100, 40, Props.white)
        self.music_is_playing = True

    def toggle_music(self):
        music = pygame.mixer.music
        if self.music_is_playing:
            music.pause()
        else:
            music.unpause()
        self.music_is_playing = not self.music_is_playing

    def load_music(self):
        try:
            intro_screen_music = pygame.mixer.music.load('sounds/Pippin.mp3')
            pygame.mixer.music.play(-1)
        except Exception as exc:
            print("Exception loading music: {}".format(exc))


