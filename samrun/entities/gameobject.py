from abc import ABC, abstractmethod
from samrun.config import cfg_item, Config
import pygame

class GameObject(pygame.sprite.Sprite, ABC):
    
    def __init__(self):
        super().__init__()
        self._position = pygame.math.Vector2(0.0,0.0)    
        self.rect = pygame.Rect(0,0,0,0)
        self.render_rect = pygame.Rect(0,0,0,0)
        
    @abstractmethod    
    def handle_input(self, key, is_pressed):
        pass
    
    @abstractmethod
    def update(self, delta_time):
        pass
    
    @abstractmethod
    def render(self, surface_dst):
        pass
    
    @abstractmethod
    def release(self):
        pass
    
          
    def _is_in_bounds(self, distance):
        new_position = self._position + distance
        
        return new_position.x >=0 and new_position.x <= cfg_item("game","screen_size")[0] and new_position.y >=0 and new_position.y <= cfg_item("game","screen_size")[1]
    
    def _center(self):
        self.rect.center = self._position.xy
        self.render_rect.center = self._position.xy
        
    def _render_debug(self, surface):
        if Config.instance().debug:
            pygame.draw.rect(surface, (255,0,0),self.rect, 1)
            pygame.draw.rect(surface, (0,255,0),self.render_rect, 1)
        
    def get_position(self):
        return self.rect.x