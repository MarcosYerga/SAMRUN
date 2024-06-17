import pygame

from samrun.states.state import State
from samrun.assets.assests_manager import AssetsManager
from samrun.config import cfg_item

class Intro(State):

    def __init__(self):
        super().__init__()
        self.next_state = "GamePlay"

    def enter(self):
        self.__render_fps_surface()

    def exit(self):
        pass

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            self.done = True

    def update(self, delta_time):
        pass

    def render(self, surface):
        surface.blit(self.__image, (100,100))

    def __render_fps_surface(self):
        font = AssetsManager.instance().get(cfg_item("font", "name"))
        self.__image = font.render(f"Press any key to Continue", True, cfg_item("game", "foreground"), None)