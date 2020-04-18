from datetime import datetime
from lib import CTDT, Config, Cache
import time
from tsubasa import Tsubasa

DEBUG = False
CTDT.initialize()
CTDT.convert_templates_to_jpeg()
config: Config = Config.get_instance()
caches: Cache = Cache.get_instance()
CTDT.initialize_cache()

print("Start Processing : {0}".format(datetime.now()))

####################################################################

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
