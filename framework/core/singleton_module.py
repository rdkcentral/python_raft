
class Singleton:
    
    _instance = None
    _config = None


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # def __init__(self):
    #     # Initialize singleton attributes
    #     self.config = None

    def set_config(self, config):
        self.config = config

    def get_config(self):
        return self.config
    