import pygame

from samrun.FPS_stats import FPS_stats
from samrun.config import cfg_item, Config
from samrun.assets.assests_manager import AssetsManager
from samrun.assets.assests import AssetType
from samrun.states.statemanager import StateManager
from samrun.assets.soundmanager import SoundManager

class Game:
    
    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()

        self.__screen = pygame.display.set_mode([cfg_item("game","screen_size")[0],cfg_item("game","screen_size")[1]], 0, 32)
        pygame.display.set_caption(cfg_item("game","name"))

        pygame.mouse.set_visible(False)

        self.__running = True
        self.__load_assets()
        self.__time_per_frame = 5000 /cfg_item("timing","fps")
        self.__fps_stats = FPS_stats()
        self.__state_manager = StateManager()
        

    def run(self):
        last_time = pygame.time.get_ticks()
        time_since_last_update = 0
        while self.__running:
            delta_time, last_time = self.__calc_delta_time(last_time)
            time_since_last_update += delta_time

            while time_since_last_update > self.__time_per_frame:
                time_since_last_update -= self.__time_per_frame
                self.__handle_input()
                self.__update(self.__time_per_frame)

            self.__render()
        self.__release()

    def __handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__running = False
                elif event.key == pygame.K_F5:
                    Config.instance().debug = not Config.instance().debug
                    
            self.__state_manager.handle_input(event)

    def __update(self, delta_time):
        self.__state_manager.update(delta_time)
        self.__fps_stats.update(delta_time)
        SoundManager.instance().update(delta_time)

    def __render(self):
        self.__screen.fill(cfg_item("game","fondo"))
        self.__state_manager.render(self.__screen)
        if Config.instance().debug:
            self.__fps_stats.render(self.__screen)
        pygame.display.flip()

    def __release(self):
        self.__state_manager.quit()
        self.__fps_stats.release()
        self.__unload_assets()
        pygame.quit()

    def __calc_delta_time(self, last_time):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_time
        return delta_time, current_time

    def __load_assets(self):
        AssetsManager.instance().load(AssetType.Font, 'main', cfg_item("font", "name"), cfg_item("font", "font_file"), font_size = cfg_item("font", "size"))

    def __unload_assets(self):
        AssetsManager.instance().clear('main')