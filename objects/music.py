import time
import pygame
from pygame import mixer

class Music(object):

    def __init__(self, type=1):
        self.type = type
        self.music = None
        mixer.init()
        mixer.music.load("./music_files/Trip.mp3")

    def _get_music_file(self):
        if self.type == 1:
            self.music = "Trip"
        return '{}.mp3'.format(self.music)

    def play(self):
        mixer.music.play(-1)

    def set_volumn(self, value):
        mixer.music.set_volume(value)

    def pause(self):
        mixer.music.pause()

    def unpause(self):
        mixer.music.unpause()


if __name__ == '__main__':
    music = Music(1)
    music.play()
    #
    # pygame.mixer.init()
    # # 加载音乐
    # pygame.mixer.music.load("../music_files/Trip.mp3")
    # while True:
    #     # 检查音乐流播放，有返回True，没有返回False
    #     # 如果没有音乐流则选择播放
    #     if pygame.mixer.music.get_busy() == False:
    #         pygame.mixer.music.play()