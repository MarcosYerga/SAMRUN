import pygame
from samrun.config import cfg_item
from samrun.assets.assests_manager import AssetsManager
class FPS_stats:

    def __init__(self):
        self.__logic_frames = 0
        self.__render_frames = 0
        self.__refresh_update_time = cfg_item("timing","refresh_time")
        self.__update_time = 0
        self.__render_fps_surface()

    def update(self, delta_time):
        self.__logic_frames += 1
        self.__update_time += delta_time

        if self.__update_time > self.__refresh_update_time:
            self.__render_fps_surface()
            self.__logic_frames = 0
            self.__render_frames = 0
            self.__update_time -= self.__refresh_update_time

    def render(self, surface_dst):
        self.__render_frames += 1
        surface_dst.blit(self.__image, cfg_item("timing","stats_pos"))

    def release(self):
        pass

    def __render_fps_surface(self):
        font = AssetsManager.instance().get(cfg_item("font","name"))
        self.__image = font.render(f"{self.__logic_frames}-{self.__render_frames}", True, cfg_item("game","foreground"), None)
        
      
        