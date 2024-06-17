from samrun.assets.background import Background

class Parallax:

    def __init__(self):
        pass

    def update(self, delta_time):
        self.__background.update(delta_time)

    def render(self, surface_dst):
        self.__background.render(surface_dst)

    def add_background(self, name, speed):
        self.__background =  Background(name, speed)
        