from samrun.assets.assests_manager import AssetsManager
from samrun.entities.gameobject import GameObject
from samrun.config import cfg_item
import pygame

class ArrowFactory:
    
    @staticmethod
    def create_arrow(position):
        return Arrow(position)

class Arrow(GameObject):

    def __init__(self, position):
        super().__init__()
        velocity = cfg_item("entities", "arrow","velocity")
        self._position = pygame.math.Vector2(position)
        self.__velocity = pygame.math.Vector2(velocity)
        self._name = cfg_item("entities", "arrow", "name")
        _, rect = AssetsManager.instance().get(self._name)

        self.render_rect = rect.copy()
        self.rect = self.render_rect.copy()

    def handle_input(self, key, is_pressed):
        pass

    def update(self, delta_time):
        distance = self.__velocity * delta_time
        self._position.x -= distance.x
        self.render_rect.topleft = self._position
        self.rect.topleft = self._position 

    def render(self, surface_dst):
        image, _ = AssetsManager.instance().get(self._name)
        flipped_image = pygame.transform.flip(image, True, False)
        surface_dst.blit(flipped_image, self.render_rect)

        self._render_debug(surface_dst)

    def release(self):
        pass