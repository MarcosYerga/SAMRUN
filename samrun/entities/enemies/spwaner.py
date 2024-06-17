import random,pygame
from samrun.entities.enemies.enemy import EnemyType
from samrun.config import cfg_item

class Spawner():
    
    def __init__(self, call_back_spawn_enemy):
        self.__call_back_spawn_enemy = call_back_spawn_enemy
        
    def update(self,delta_time):
        if random.random() <= 0.04:
            enemy_type = EnemyType.Mele if random.randint(0,1) == 0 else EnemyType.Archer
            spawn_point = pygame.math.Vector2(1200,250)
            
            self.__call_back_spawn_enemy(enemy_type, spawn_point)