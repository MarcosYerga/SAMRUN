import pygame
from samrun.entities.hero.run import Run
from samrun.entities.hero.jump import Jump
from samrun.entities.hero.attack1 import Attack1
from samrun.entities.hero.attack2 import Attack2
from samrun.entities.hero.shield import Shield
from samrun.entities.hero.dead import Dead

class HeroManager:
    
    def __init__(self):
        self.__hero_states= {
            "Run": Run(),
            "Jump": Jump(),
            "Attack1":Attack1(),
            "Attack2": Attack2(),
            "Shield":Shield(),
            "Dead":Dead()
        }
        
        self.__current_state_name = 'Run'
        self.__current_state = self.__hero_states[self.__current_state_name]
        self.__current_state.enter()
        
    def handle_input(self,key, is_pressed):
            self.__current_state.handle_input(key, is_pressed)

    def update(self, delta_time):
        if self.__current_state.done:
            self.__change_state()
        self.__current_state.update(delta_time)

    def render(self, surface):
        self.__current_state.render(surface)

    def quit(self):
        self.__current_state.exit()

    def __change_state(self):
        self.__current_state.exit()

        previous_state = self.__current_state_name
        self.__current_state_name = self.__current_state.next_state
        self.__current_state = self.__hero_states[self.__current_state_name]
        self.__current_state.previous_state = previous_state

        self.__current_state.done = False
        self.__current_state.enter()
        
    def get_rect(self):
        return self.__current_state.get_rect()
    
    def get_state(self):
        return self.__current_state_name
    
    def hero_dead(self):
        self.__current_state.done = True
        self.__current_state.next_state = "Dead"
        
        