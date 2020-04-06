from datetime import datetime
from lib import CTDT, Config, Cache
import time
from story_solo import StorySolo

CTDT.convert_templates_to_jpeg()
config: Config = Config.get_instance()
caches: Cache = Cache.get_instance()
CTDT.initialize_cache()

print("Start Processing : {0}".format(datetime.now()))

####################################################################

# Story Solo = 1
if config.mode == 1:

    while True:
        StorySolo.run()
        time.sleep(config.sleep)
