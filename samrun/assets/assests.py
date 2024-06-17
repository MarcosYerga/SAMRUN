from enum import Enum
import pygame

class AssetType(Enum):
    Image = 0,
    Spritesheet = 1,
    Font = 2,
    Sound = 3,
    Music = 4,   
    
class Asset:
    
    def __init__(self, asset_type, category):
        self.payload = None
        self.asset_type = asset_type
        self.category = category
        
    def load(self, asset_filename_path , font_size=0,cols = 0):
        if self.asset_type == AssetType.Image:
            self.payload = pygame.image.load(asset_filename_path).convert_alpha()
        elif self.asset_type == AssetType.Font:
            self.payload = pygame.font.Font(asset_filename_path, font_size)
        elif self.asset_type == AssetType.Sound:
            self.payload = pygame.mixer.Sound(asset_filename_path)
        elif self.asset_type == AssetType.Music:
            self.payload = asset_filename_path
        