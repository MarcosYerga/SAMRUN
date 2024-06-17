from abc import ABC,abstractmethod
from samrun.config import cfg_item
import pygame
    
class HeroState(ABC):
    def __init__(self):
        self.done = False
        self.next_state = ""
        self.previous_state = ""
        self.imagen_index = 0
        self.render_rect = pygame.Rect(0,0,0,0)
        self.position = pygame.math.Vector2(0,250)
        self.screen = pygame.display.set_mode([cfg_item("game","screen_size")[0],cfg_item("game","screen_size")[1]], 0, 32)
        
    @abstractmethod
    def enter(self):
        pass
    
    @abstractmethod
    def exit(self):
        pass
    
    
    def get_images(self, hero, col):
        images = []
        sprite_width = hero.get_width() // col
        sprite_height = hero.get_height()
        for column in range(col):
            rect = pygame.Rect(column * sprite_width, 0, sprite_width, sprite_height)
            imagen = hero.subsurface(rect)
            images.append(imagen)
        return images
    
    def map_input(self):
        self.key_mapping = {}
        k_map = cfg_item("input","key_maping")
        for k, v in k_map.items():
            self.key_mapping[k] = pygame.key.key_code(v)
        return self.key_mapping
    
    def get_rect(self):
        return  self.render_rect,self.rect