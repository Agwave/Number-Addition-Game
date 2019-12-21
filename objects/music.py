from pygame import mixer

class Music(object):

    def __init__(self, type=1):
        self.type = type
        self.music = None
        mixer.init()
        mixer.music.load("./music_files/Trip.mp3")

    def play(self, loop=-1):
        mixer.music.play(loop)

    def set_volumn(self, value):
        mixer.music.set_volume(value)

    def pause(self):
        mixer.music.pause()

    def unpause(self):
        mixer.music.unpause()