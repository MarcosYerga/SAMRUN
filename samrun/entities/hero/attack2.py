from samrun.entities.hero.herostates import HeroState
from samrun.assets.assests_manager import AssetsManager
from samrun.assets.assests import AssetType
from samrun.assets.soundmanager import SoundManager
from samrun.config import cfg_item
import pygame

class Attack2(HeroState):
    def __init__(self):
        super().__init__()
        self.next_state = ""
        self.__load_assets()
        self.__hero, _ =AssetsManager.instance().get("ATTACK2")
        self.__columns = cfg_item("entities","hero","attack2_col")
        self.__images = self.get_images(self.__hero,self.__columns)
        self.rect = self.__images[0].get_rect()
        self.rect.y = self.position.y
        self.__imagen_index = 0
        self.render_rect = self.rect.copy()
        self.rect=pygame.Rect(self.position.x,self.position.y+50,self.render_rect.width,self.render_rect.height)

    def enter (self):
        self.render(self.screen)
        SoundManager.instance().play_sound(cfg_item("sfx","attack","name"))
        self.__imagen_index = 0
    def exit(self):
        pass

    def handle_input(self, key, is_pressed):
        pass

    def update(self, delta_time):
        if self.__imagen_index < len(self.__images) - 1:
            self.__imagen_index += 1
        else:
            self.next_state = "Run"
            self.done = True
             
    def render(self, surface):
        self.__image = self.__images[self.__imagen_index]
        surface.blit(self.__image, self.render_rect)

    def __load_assets(self):
        AssetsManager.instance().load(AssetType.Image, 'main', "ATTACK2", cfg_item("entities", "hero","attack2"))