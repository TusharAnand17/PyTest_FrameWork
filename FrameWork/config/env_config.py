import yaml

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            with open("config/config.yaml") as f:
                cls._instance = yaml.safe_load(f)
        return cls._instance