from samrun.entities.hero.herostates import HeroState
from samrun.assets.assests_manager import AssetsManager
from samrun.assets.assests import AssetType
from samrun.config import cfg_item
from samrun.assets.soundmanager import SoundManager
import pygame

class Dead(HeroState):
    def __init__(self):
        super().__init__()
        self.__load_assets()
        self.__hero, rect =AssetsManager.instance().get("DEAD")
        self.__columns = cfg_item("entities","hero","dead_col")
        self.__images = self.get_images(self.__hero,self.__columns)
        self.rect = rect.copy()
        self.rect = self.__images[0].get_rect()
        self.rect.y = self.position.y
        self.__imagen_index = 0
        self.render_rect = self.rect.copy()
        self.rect=pygame.Rect(self.position.x,self.position.y,self.render_rect.width*0.5,self.render_rect.height*0.5)

    def enter (self):
        self.render(self.screen)
        self.__imagen_index = 0
        SoundManager.instance().play_sound(cfg_item("sfx","hit","name"))
    def exit(self):
        pass

    def handle_input(self, key, is_pressed):
        pass

    def update(self, delta_time):
        for self.__imagen_index in range(len(self.__images)):
            self.render(self.screen)
             
    def render(self, surface):
        self.__image = self.__images[self.__imagen_index]
        surface.blit(self.__image, self.render_rect)

    def __load_assets(self):
        AssetsManager.instance().load(AssetType.Image, 'main', "DEAD", cfg_item("entities", "hero","dead"))