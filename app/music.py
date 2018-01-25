


from app.sprites import Button
from app.properties import Properties as Props
import pygame





class Music(object):
    def __init__(self):
        self.music_button = Button("TOGGLE MUSIC", Props.SCREENLENGTH * .9, 0, 100, 40, Props.white)
        self.music_is_playing = True
        self.playlist = ['sounds/Pippin.ogg','sounds/Hidden_Past.ogg', 'sounds/Thatched_Villagers.ogg', 'sounds/Mountain_Emperor.ogg',
                         'sounds/Moorland.ogg','sounds/Galway.ogg', 'sounds/Angevin_B.ogg']
        self.first_song = self.playlist[0]
        self.song_end = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.song_end)

    def toggle_music(self):
        music = pygame.mixer.music
        if self.music_is_playing:
            music.pause()
        else:
            music.unpause()
        self.music_is_playing = not self.music_is_playing

    def play_first_song(self):
        pygame.mixer.music.load(self.first_song)
        pygame.mixer.music.play()
        print("first song is playing.")
        finished_song = self.playlist.pop(0)
        self.playlist.append(finished_song)

    def play_next_song(self):
        try:
            a = self.playlist[0]
            pygame.mixer.music.load(a)
            pygame.mixer.music.play()
            b = self.playlist.pop(0)
            self.playlist.append(b)

        except Exception as exc:
            print("Exception loading music: {}".format(exc))


