from importlib import resources
from os import path
from samrun.assets.assests import Asset, AssetType
class AssetsManager:
    
    __instance = None
    
    @staticmethod
    def instance():
        if AssetsManager.__instance is None:
            AssetsManager()
        return AssetsManager.__instance
    
    def __init__(self):
        if AssetsManager.__instance is None:
            AssetsManager.__instance = self
            
            self.__assests = {} 
        else:
            raise Exception("Solo puede haber una instancia de configuracion")
        
    def load(self, asset_type, category,asset_name,asset_filename,font_size = 0,cols = 0):
        with resources.path(asset_filename[0],asset_filename[1])as asset_path:
            if path.isfile(asset_path) and asset_name not in self.__assests:
                asset = Asset(asset_type,category)
                asset.load(asset_path, font_size,cols)
                self.__assests[asset_name] = asset
              
    def get(self, asset_name):
        if asset_name in self.__assests:
            if self.__assests[asset_name].asset_type == AssetType.Image:
                return self.__assests[asset_name].payload, self.__assests[asset_name].payload.get_rect()
            else:
                return self.__assests[asset_name].payload
        else:
            return None
        
        
    def clear(self, category = None):
        if category:
            for k in list(self.__assests.keys()):
                if self.__assests[k].category == category:
                    del self.__assests[k]
        else:
            self.__assests={}
