from importlib import resources
import json

def cfg_item(*items):
    data = Config.instance().data
    for key in items:
        data = data[key]
    return data

class Config:
    
    __config_json_path, __config_json_filename = "samrun.assets.config","config.json"
    __instance = None
    
    @staticmethod
    def instance():
        if Config.__instance is None:
            Config()
        return Config.__instance
    
    def __init__(self):
        if Config.__instance is None:
            Config.__instance = self
            
            with resources.path(Config.__config_json_path,Config.__config_json_filename) as json_file:
                with open(json_file) as file:
                    self.data = json.load(file)
            self.__debug = False
        else:
            raise Exception("Solo puede haber una instancia de configuracion")
    
    @property
    def debug(self):
        return self.__debug

    @debug.setter
    def debug(self, value):
        self.__debug = value