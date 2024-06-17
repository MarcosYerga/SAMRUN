import pygame

from samrun.assets.assests_manager import AssetsManager
from samrun.config import cfg_item

class SoundManager:

    __instance = None

    @staticmethod
    def instance():
        if SoundManager.__instance is None:
            SoundManager()
        return SoundManager.__instance

    def __init__(self):
        if SoundManager.__instance is None:
            SoundManager.__instance = self

            self.__sound_volume = cfg_item("sfx", "volume")
            self.__music_volume = cfg_item("music", "volume")

            self.__current_music = None
            self.__next_music = None

        else:
            raise Exception("There Can Be Only One Instance of SoundManager")

    def play_sound(self, name):
        sound = AssetsManager.instance().get(name)
        sound.set_volume(self.__sound_volume)
        sound.play()

    def play_music(self, name):
        if name is self.__current_music:
            return

        music = AssetsManager.instance().get(name)
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(self.__music_volume)
        self.__current_music = name
        pygame.mixer.music.play(-1)

    def stop_music(self, time = 100):
        pygame.mixer.music.fadeout(time)
        self.__current_music = None

    def play_music_fade(self, name):
        if name is self.__current_music:
            return

        self.__next_music = name
        pygame.mixer.music.fadeout(cfg_item("music", "fadeout"))

    def update(self, delta_time):
        if self.__next_music is not None and not pygame.mixer.music.get_busy():
            self.play_music(self.__next_music)
            self.__current_music = self.__next_music
            self.__next_music = None