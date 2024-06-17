import pygame

from samrun.states.state import State
from samrun.entities.hero.hero import Hero
from samrun.entities.rendergroup import RenderGroup
from samrun.assets.assests_manager import AssetsManager
from samrun.assets.assests import AssetType
from samrun.config import cfg_item
from samrun.assets.soundmanager import SoundManager
from samrun.entities.enemies.spwaner import Spawner
from samrun.entities.enemies.pool import Pool
from samrun.entities.enemies.enemy import Enemy
from samrun.assets.parallax import Parallax
from samrun.entities.enemies.spwaner import Spawner
from samrun.entities.enemies.arrow import ArrowFactory
from samrun.entities.obstacules.floor import Floor

class Gameplay(State):

    def __init__(self):
        super().__init__()
        self.next_state = "Game Over"
        self.__enemy_pool = Pool(Enemy, 2)
        self.__players = RenderGroup()
        self.__enemies = RenderGroup()
        self.__enemy_arrows=RenderGroup()
        self.__load_assets()

        self.__players.add(Hero())
        self.__spawner = Spawner(self.__spawn_enemy)
        SoundManager.instance().play_music(cfg_item("music", "mission", "name"))
        self.__parallax = Parallax()
        self.__parallax.add_background(cfg_item("backgrounds", "forest", "name"), cfg_item("backgrounds", "forest", "speed"))
        self.__floor = Floor()

    def enter(self):
        self.__load_assets()

        self.__players.add(Hero())
        SoundManager.instance().play_music(cfg_item("music", "mission", "name"))
        self.__spawner = Spawner(self.__spawn_enemy)
        self.__parallax = Parallax()
        self.__parallax.add_background(cfg_item("backgrounds", "forest", "name"), cfg_item("backgrounds", "forest", "speed"))
    
    def exit(self):
        for enemy in self.__enemies:
            self.__enemy_pool.release(enemy)

        self.__players.empty()
        self.__enemies.empty()
        self.__enemy_arrows.empty()
        self.__spawner = None
        SoundManager.instance().stop_music()
        self.__unload_assets()

        
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            self.__players.handle_input(event.key, True)
        if event.type == pygame.KEYUP:
            self.__players.handle_input(event.key, False)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.done = True
 
        
    def update(self, delta_time):
        self.__players.update(delta_time)
        self.__parallax.update(delta_time)
        self.__enemies.update(delta_time)
        self.__spawner.update(delta_time)
        self.__enemy_arrows.update(delta_time)
        for player in self.__players.sprites():
            if isinstance(player, Hero) and player.get_state_name() == "Attack1":
                collided_enemies = pygame.sprite.spritecollide(player, self.__enemies, False)
                for enemy in collided_enemies:
                    if isinstance(enemy,Enemy):
                        enemy.dead_enemy()
            elif isinstance(player, Hero) and player.get_state_name() == "Attack2":
                collided_enemies = pygame.sprite.spritecollide(player, self.__enemies, False)
                for enemy in collided_enemies:
                    if isinstance(enemy,Enemy):
                        enemy.dead_enemy()
            elif isinstance(player, Hero) and player.get_state_name() == "Shield":
                pygame.sprite.spritecollide(player, self.__enemy_arrows, True)
                                          
            
        for player in pygame.sprite.groupcollide(self.__players, self.__enemies, False, False).keys():
            if isinstance(player, Hero):
                player.hero_dead()
                player.update(delta_time)
            self.__game_over()
        
        for player in pygame.sprite.groupcollide(self.__players, self.__enemy_arrows, False, False).keys():
            if isinstance(player, Hero):
                player.hero_dead()
                player.update(delta_time)
            self.__game_over()
    
        
        
    def render(self, surface):
        self.__parallax.render(surface)
        self.__floor.render(surface)
        self.__players.draw(surface)
        self.__enemies.draw(surface)
        self.__enemy_arrows.draw(surface)


    def __load_assets(self):
        AssetsManager.instance().load(AssetType.Music, 'gameplay', cfg_item("music", "mission", "name"), cfg_item("music", "mission", "file"))
        AssetsManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "jump", "name"), cfg_item("sfx", "jump", "file"))
        AssetsManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "attack", "name"), cfg_item("sfx", "attack", "file"))
        AssetsManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "defence", "name"), cfg_item("sfx", "defence", "file"))
        AssetsManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "hit", "name"), cfg_item("sfx", "hit", "file"))
        AssetsManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "archer", "name"), cfg_item("sfx", "archer", "file"))
        AssetsManager.instance().load(AssetType.Sound, 'gameplay', cfg_item("sfx", "pain", "name"), cfg_item("sfx", "pain", "file"))
        AssetsManager.instance().load(AssetType.Image, 'gameplay', cfg_item("backgrounds", "forest", "name"),(cfg_item("backgrounds", "forest", "image_file"))) 
        AssetsManager.instance().load(AssetType.Image, 'gameplay', cfg_item("floor","name"),(cfg_item("floor", "image_file")))
        AssetsManager.instance().load(AssetType.Image,"gameplay",cfg_item("entities","arrow","name"),cfg_item("entities","arrow","image_file"))
    
    def __unload_assets(self):
        AssetsManager.instance().clear("gameplay")

    def __spawn_enemy(self, enemy_type,spawn_point):
        enemy = self.__enemy_pool.acquire()
        self.__hero_pos = self.get_hero_pos()
        enemy.init(enemy_type,spawn_point,self.__kill_enemy,self.__hero_pos,self.__spawn_arrows)
        self.__enemies.add(enemy)
    
    def __kill_enemy(self, enemy):
        self.__enemies.remove(enemy)
        self.__enemy_pool.release(enemy)
    
    def __game_over(self):
        print("GAME OVER")
        self.done=True
        
    def get_hero_pos(self):
         for player in self.__players.sprites():
                if isinstance(player, Hero):
                    return player.get_position()
                else:
                    return 0
                
    def __spawn_arrows(self, position):
            self.__enemy_arrows.add(ArrowFactory.create_arrow(position))
            SoundManager.instance().play_sound(cfg_item("sfx", "archer", "name"))