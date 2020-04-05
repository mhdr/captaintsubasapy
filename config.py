import configparser


class Config:
    __instance = None
    mode: int
    sleep: float

    @staticmethod
    def get_instance():
        """
        static access method
        :return: Template
        """
        if Config.__instance is None:
            config = configparser.ConfigParser()
            config.read('config.ini')

            Config.mode = int(config["Game"]["Mode"])
            Config.sleep = float(config["General"]["Sleep"])

            Config()

        return Config.__instance

    def __init__(self):
        """
        Virtually private constructor
        """
        Config.__instance = self
