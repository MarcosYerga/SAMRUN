import pygame
from samrun.entities.gameobject import GameObject
from samrun.entities.hero.heromanager import HeroManager


class Hero(GameObject):
    
    def __init__(self) :
        super().__init__()   
        self._position = pygame.math.Vector2(0,250)        
        self.__hero = HeroManager()
        self.__hero_state ="" 
        
    def handle_input(self, key, is_pressed):
        self.__hero.handle_input(key, is_pressed)
    
    def update(self, delta_time):
        self.__hero.update(delta_time)
        self.__hero_state = self.__hero.get_state()
        self.render_rect,self.rect = self.__hero.get_rect()
        
    def render(self, surface_dst):
        self.__hero.render(surface_dst)
        self._render_debug(surface_dst)
    
    def release(self):
        pass
    
    def get_state_name (self):
        return self.__hero_state
    
    def hero_dead(self):
        self.__hero.hero_dead()
        