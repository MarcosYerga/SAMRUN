from samrun.entities.gameobject import GameObject
from samrun.entities.enemies.pool import ReusableObject
from samrun.assets.assests_manager import AssetsManager
from samrun.assets.soundmanager import SoundManager
from samrun.assets.assests import AssetType
from samrun.config import cfg_item
from enum import Enum
import pygame

class EnemyType(Enum):
    Archer = 0,
    Mele = 1

class EnemyState(Enum):
    Main = 0
    Attack = 1
    Dead = 2

class Enemy(GameObject, ReusableObject):
    
    def __init__(self) :
        super().__init__()
        self.__enemy_name = ""
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.__imagen_index = 0
        
    def init(self, enemy_type , spawn_point  ,callback_kill_enemy, hero_pos, callback_spawn_arrow):
        self.___enemy_type = enemy_type
        self.__callback_kill_enemy = callback_kill_enemy
        self.__spawn_arrow = callback_spawn_arrow
        self.__columns = 0
        if self.___enemy_type == EnemyType.Archer:
            self.__enemy_name = cfg_item("entities","enemies","archer","name")
            self.__columns = cfg_item("entities","enemies","archer","idle","columns")
        elif self.___enemy_type == EnemyType.Mele:
            self.__enemy_name = cfg_item("entities","enemies","mele","name")
            self.__columns = cfg_item("entities","enemies","mele","run","columns")
            
        self.__load_assets()
        self.__enemy, _ = AssetsManager.instance().get(cfg_item("entities", "enemies",self.__enemy_name,"name"))
        self.__images = self.__get_images(self.__enemy,self.__columns)
        self.render_rect = self.__images[0].get_rect()
        self.render_rect.x = spawn_point.x
        self.render_rect.y = spawn_point.y
        self.rect = self.render_rect.copy()
        self.rect=pygame.Rect(self.render_rect.x +50, self.render_rect.y+60, self.rect.width * 0.5, self.rect.height * 0.5)
        self.__imagen_index = 0
        self.__enemy_state = EnemyState.Main
        self.__cool_down_time = cfg_item("entities","enemies","archer","cool_down")
        self.__cool_down = 0
        self.__hero_pos = hero_pos
    def reset(self):
        self.__enemy_name = ""
        self.rect = pygame.Rect(0,0,0,0)
        self.__imagen_index = 0
        
    def handle_input(self, key, is_pressed):
        pass
    
    def update(self, delta_time):
        self.__body_update(delta_time)
    
    def __body_update(self, delta_time):
        self._position.x = self.rect.x
        self._position.y = self.rect.y
        velocity = pygame.math.Vector2(0.0, 0.0)
        self.__cool_down -= delta_time

        if self.__enemy_name == "mele":
            speed = 0.3
        elif self.__enemy_name == "archer":
           speed = 0.2

        velocity.x += speed
        distance = velocity * delta_time

        self.render_rect.x -= distance.x
        self.rect.x -= distance.x 

        self.__load_images()

        if self.__enemy_state == EnemyState.Main:
            if self.__imagen_index < len(self.__images) - 1:
                self.__imagen_index += 1
            else:
                self.__imagen_index = 0
                if self.__enemy_name == "archer" and self.__cool_down <= 0.0:
                    self.__enemy_state = EnemyState.Attack
                    self.__cool_down = self.__cool_down_time
            if self.__enemy_name == "mele" and self.rect.x-self.__hero_pos <= 100:
                self.__enemy_state = EnemyState.Attack
        elif self.__enemy_state == EnemyState.Attack:
            if self.__imagen_index < len(self.__images) - 1:
                self.__imagen_index += 1
            else:
                self.__imagen_index = 0
                if self.__enemy_name == "archer":
                    self.__spawn_arrow( self._position)
                self.__enemy_state = EnemyState.Main   
        elif self.__enemy_state == EnemyState.Dead:
            if self.__imagen_index < len(self.__images) - 1:
                self.__imagen_index += 1
            else:
                self.kill_enemy()
        
        if self.rect.x < 0:
            self.kill_enemy()
        
    def render(self, surface_dst):
        self.__image = self.__images[self.__imagen_index]
        flipped_image = pygame.transform.flip(self.__image, True, False)

        surface_dst.blit(flipped_image,self.render_rect)
        self._render_debug(surface_dst)
        
    def release(self):
        pass
    
    def kill_enemy(self):
        self.__callback_kill_enemy(self)
        
    def __load_assets(self):
       AssetsManager.instance().load(AssetType.Image, 'main', cfg_item("entities","enemies","archer","name"), cfg_item("entities","enemies","archer","idle","image_file"))
       AssetsManager.instance().load(AssetType.Image, 'main', cfg_item("entities","enemies","archer","name2"), cfg_item("entities","enemies","archer","attack","image_file"))
       AssetsManager.instance().load(AssetType.Image, 'main', cfg_item("entities","enemies","archer","name3"), cfg_item("entities","enemies","archer","dead","image_file"))
       
       AssetsManager.instance().load(AssetType.Image, 'main', cfg_item("entities","enemies","mele","name"), cfg_item("entities","enemies","mele","run","image_file"))
       AssetsManager.instance().load(AssetType.Image, 'main', cfg_item("entities","enemies","mele","name2"), cfg_item("entities","enemies","mele","attack","image_file"))
       AssetsManager.instance().load(AssetType.Image, 'main', cfg_item("entities","enemies","mele","name3"), cfg_item("entities","enemies","mele","dead","image_file"))
       
    def __load_images(self):
        if self.__enemy_name == "mele":
            if self.__enemy_state == EnemyState.Main:
                self.__enemy, _ = AssetsManager.instance().get(cfg_item("entities", "enemies",self.__enemy_name,"name"))
                self.__columns = cfg_item("entities","enemies","mele","run","columns")
                self.__images = self.__get_images(self.__enemy,self.__columns)
            elif self.__enemy_state ==EnemyState.Attack:
                self.__enemy, _ = AssetsManager.instance().get(cfg_item("entities", "enemies",self.__enemy_name,"name2"))
                self.__columns = cfg_item("entities","enemies","mele","attack","columns")
                self.__images = self.__get_images(self.__enemy,self.__columns)
            elif self.__enemy_state == EnemyState.Dead:
                self.__enemy, _ = AssetsManager.instance().get(cfg_item("entities", "enemies",self.__enemy_name,"name3"))
                self.__columns = cfg_item("entities","enemies","mele","dead","columns")
                self.__images = self.__get_images(self.__enemy,self.__columns)        
        
        elif self.__enemy_name == "archer":
            if self.__enemy_state == EnemyState.Main:
                self.__enemy, _ = AssetsManager.instance().get(cfg_item("entities", "enemies",self.__enemy_name,"name"))
                self.__columns = cfg_item("entities","enemies","archer","idle","columns")
                self.__images = self.__get_images(self.__enemy,self.__columns)
            elif self.__enemy_state ==EnemyState.Attack:
                self.__enemy, _ = AssetsManager.instance().get(cfg_item("entities", "enemies",self.__enemy_name,"name2"))
                self.__columns = cfg_item("entities","enemies","archer","attack","columns")
                self.__images = self.__get_images(self.__enemy,self.__columns)
            elif self.__enemy_state == EnemyState.Dead:
                self.__enemy, _ = AssetsManager.instance().get(cfg_item("entities", "enemies",self.__enemy_name,"name3"))
                self.__columns = cfg_item("entities","enemies","archer","dead","columns")
                self.__images = self.__get_images(self.__enemy,self.__columns)
    
    def __get_images(self, enemy, col):
        images = []
        sprite_width = enemy.get_width() // col
        sprite_height = enemy.get_height()
        for column in range(col):
            rect = pygame.Rect(column * sprite_width, 0, sprite_width, sprite_height)
            imagen = enemy.subsurface(rect)
            images.append(imagen)
        return images
    
    def dead_enemy (self):
        SoundManager.instance().play_sound(cfg_item("sfx", "pain", "name"))
        self.rect = pygame.Rect(0,0,0,0)
        self.__imagen_index = 0
        self.__enemy_state = EnemyState.Dead