from datetime import datetime
from lib import CTDT, Config, Cache
import time
from telegram_bot import TelegramBot
from tsubasa import Tsubasa

DEBUG = False
CTDT.initialize()
config: Config = Config.get_instance()
caches: Cache = Cache.get_instance()
CTDT.convert_templates_to_jpeg()
CTDT.initialize_cache()

print("Start Processing : {0}".format(datetime.now()))

####################################################################

if __name__ == "__main__":
    # execute only if run as a script

    telegram:TelegramBot = TelegramBot(config.telegram_token, config.telegram_disabled)
    tsubasa: Tsubasa = Tsubasa()

    while True:

        if DEBUG:
            result = tsubasa.run()
            print(result)
            time.sleep(config.sleep)
        else:
            try:
                result = tsubasa.run()
                time.sleep(config.sleep)
            except Exception as ex:
                print(str(ex))
