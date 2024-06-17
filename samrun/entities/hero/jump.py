from samrun.entities.hero.herostates import HeroState
from samrun.assets.assests_manager import AssetsManager
from samrun.assets.assests import AssetType
from samrun.assets.soundmanager import SoundManager
import pygame
from samrun.config import cfg_item

class Jump(HeroState):
    def __init__(self):
        super().__init__()
        self.next_state = ""
        self.__load_assets()
        self.__hero, _ =AssetsManager.instance().get("JUMP")
        self.__columns = cfg_item("entities","hero","jump_col")
        self.__images = self.get_images(self.__hero,self.__columns)
        self.rect = self.__images[0].get_rect()
        self.rect.y = self.position.y
        self.__imagen_index = 0
        self.render_rect = self.rect.copy()
        self.rect=pygame.Rect(self.position.x+50,self.position.y+50,self.render_rect.width*0.2,self.render_rect.height*0.2)
        
    def enter (self):        
        self.render(self.screen)
        self.__imagen_index = 0
        SoundManager.instance().play_sound(cfg_item("sfx","jump","name"))
        
    def exit(self):
        pass

    def handle_input(self, key, is_pressed):
        pass

    def update(self, delta_time):
        velocity = pygame.math.Vector2(0.0, 0.0)
        speed = cfg_item("entities","hero","speed")
        velocity.y += speed

        distance = velocity * delta_time  
        if self.__imagen_index < len(self.__images) - 1:
            self.__imagen_index += 1
            if self.rect.y >200:
                self.render_rect.y -= distance.y
                self.rect.y -= distance.y

        else:
            self.rect.y += distance.y
            self.render_rect.y += distance.y
            if self.render_rect.y == self.position.y:         
                self.next_state = "Run"
                self.done = True
            

    def render(self, surface):
            self.__image = self.__images[self.__imagen_index]
            surface.blit(self.__image, self.render_rect)

    def __load_assets(self):
        AssetsManager.instance().load(AssetType.Image, 'main', "JUMP", cfg_item("entities", "hero","jump"))