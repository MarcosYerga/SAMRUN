from samrun.assets.assests_manager import AssetsManager
from samrun.config import cfg_item
from samrun.entities.gameobject import GameObject

class Floor(GameObject):
    
    def __init__(self):
        super().__init__()
        self.__image, rect = AssetsManager.instance().get(cfg_item("floor","name"))
        self.rect = rect
        self.rect.y = 370
         
    def handle_input(self, key, is_pressed):
        pass
    
    def update(self, delta_time):
        pass
    
    def render(self, surface_dst):
        surface_dst.blit(self.__image,self.rect)
    
    def release(self):
        pass