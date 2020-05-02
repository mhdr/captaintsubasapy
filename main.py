from datetime import datetime
from lib import CTDT, Config, Cache
import time
from telegram_bot import TelegramBot
from tsubasa import Tsubasa
import sys

# wait before restarting bot
if "-r" in sys.argv:
    time.sleep(5)

DEBUG = False
CTDT.initialize()
config: Config = Config.get_instance()
caches: Cache = Cache.get_instance()
CTDT.convert_templates_to_jpeg()
CTDT.initialize_cache()

telegram: TelegramBot = TelegramBot()
tsubasa: Tsubasa = Tsubasa()

print("Start Processing : {0}".format(datetime.now()))


####################################################################

def callback_exit_app():
    telegram.reset_exit_app()


####################################################################

def callback_force_exit_app():
    telegram.reset_force_exit_app()


####################################################################

if __name__ == "__main__":
    # execute only if run as a script

    while True:

        # if pause command from bot we should continue loop
        if telegram.is_pause:
            time.sleep(config.sleep)
            continue

        if telegram.exit_app:
            tsubasa.exit_app = True
            tsubasa.set_callback_exit_app(callback_exit_app)

        if telegram.force_exit_app:
            tsubasa.force_exit_app = True
            tsubasa.set_callback_force_exit_app(callback_force_exit_app)

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
