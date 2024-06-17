from samrun.entities.hero.herostates import HeroState
from samrun.assets.assests_manager import AssetsManager
from samrun.assets.assests import AssetType
from samrun.config import cfg_item
import pygame

class Run(HeroState):
    def __init__(self):
        super().__init__()
        self.next_state = ""
        self.__load_assets()
        self.__hero, _ =AssetsManager.instance().get("RUN")
        self.__columns = cfg_item("entities","hero","run_col")
        self.__images = self.get_images(self.__hero,self.__columns)
        self.rect = self.__images[0].get_rect()
        self.rect.y = self.position.y
        self.__imagen_index = 0
        self.render_rect = self.rect.copy()
        self.rect=pygame.Rect(self.position.x,self.position.y+50,self.render_rect.width*0.5,self.render_rect.height*0.5)
        
        self.__key_mapping = self.map_input()
        
        self.cool_down_attack1_time = cfg_item("entities","hero","cooldown_attack1")
        self.cool_down_attack1 = 0
        
        self.cool_down_attack2_time = cfg_item("entities","hero","cooldown_attack2")
        self.cool_down_attack2 = 0
        
        self.cool_down_defence_time = cfg_item("entities","hero","cooldown_defence")
        self.cool_down_defence = 0
        
    def enter (self):
        self.render(self.screen)
    
    def exit(self):
        pass

    def handle_input(self, key, is_pressed):
        if key == self.__key_mapping["up"]:
            self.next_state = "Jump"
            self.done = True
        elif key == self.__key_mapping["attack1"]:
            if self.cool_down_attack1 <=0.0:
                self.next_state = "Attack1"
                self.cool_down_attack1 = self.cool_down_attack1_time
                self.done = True       
        elif key == self.__key_mapping["attack2"]:
            if self.cool_down_attack2 <=0.0:
                self.next_state = "Attack2"
                self.cool_down_attack2 = self.cool_down_attack2_time
                self.done = True
        elif key == self.__key_mapping["shield"]:
            if self.cool_down_defence <=0.0:
                self.next_state = "Shield"
                self.cool_down_defence = self.cool_down_defence_time
                self.done = True
                
    def update(self, delta_time):
            if self.__imagen_index < len(self.__images) - 1:
                self.__imagen_index += 1
            else:
                self.__imagen_index = 0
                
            if self.cool_down_attack1 >= 0.0:
                self.cool_down_attack1 -= delta_time
                
            if self.cool_down_attack2 >= 0.0:
                self.cool_down_attack2 -= delta_time
                
            if self.cool_down_defence >= 0.0:
                self.cool_down_defence -= delta_time
    
            
                
    def render(self, surface):
        self.__image = self.__images[self.__imagen_index]
        surface.blit(self.__image, self.render_rect)
            
    def __load_assets(self):
        AssetsManager.instance().load(AssetType.Image, 'main', "RUN", cfg_item("entities", "hero","run"))