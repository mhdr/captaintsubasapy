from datetime import datetime
from lib import CTDT, Config, Cache
import time
from telegram_bot import TelegramBot
from tsubasa import Tsubasa
import sys

# wait before restarting bot
if "-r" in sys.argv:
    time.sleep(5)

DEBUG = True
CTDT.initialize()
config: Config = Config.get_instance()
caches: Cache = Cache.get_instance()
CTDT.convert_templates_to_jpeg()
CTDT.initialize_cache()

telegram: TelegramBot = TelegramBot()
tsubasa: Tsubasa = Tsubasa(telegram)

print("Start Processing : {0}".format(datetime.now()))

if __name__ == "__main__":
    # execute only if run as a script

    while True:

        if DEBUG:
            result = tsubasa.run()
            if result is not None:
                print("Run => {0} : {1}, ".format(result,datetime.now()))
            time.sleep(config.sleep)
        else:
            try:
                result = tsubasa.run()
                time.sleep(config.sleep)
            except Exception as ex:
                print(str(ex))
