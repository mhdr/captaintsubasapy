from datetime import datetime
from config import Config
from lib import CTDT
from cache import Cache
import time
from story_solo import StorySolo

CTDT.convert_templates_to_jpeg()
caches: Cache = Cache.get_instance()
CTDT.initialize_cache()
config: Config = Config.get_instance()

print("Start Processing : {0}".format(datetime.now()))

####################################################################
# Solo = 11
if config.mode == 11:

    while True:
        StorySolo.run()
        time.sleep(config.sleep)
