from samrun.assets.assests_manager import AssetsManager


import pygame

class Background:
    def __init__(self, name, speed):
        self.__name = name
        self.__speed = speed

        _, rect = AssetsManager.instance().get(self.__name)

        self.__width = rect.width
        self.__x_1 = 0
        self.__x_2 = self.__width

    def update(self, delta_time):
        self.__x_1 -= self.__speed * delta_time
        self.__x_2 -= self.__speed * delta_time

       
        if self.__x_1 <= -self.__width:
            self.__x_1 = self.__x_2 + self.__width
        if self.__x_2 <= -self.__width:
            self.__x_2 = self.__x_1 + self.__width 

    def render(self, surface_dst):
        image, rect = AssetsManager.instance().get(self.__name)
        self.__render_bg(surface_dst, image, rect.copy(), self.__x_1)
        self.__render_bg(surface_dst, image, rect.copy(), self.__x_2)

    def __render_bg(self, surface_dst, surface_src, rect, x):
        rect.x = x
        surface_dst.blit(surface_src, rect)