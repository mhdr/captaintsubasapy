from datetime import datetime
from config import Config
from lib import CTDT
from template import Template
import time
from tsubasa import Tsubasa

CTDT.convert_templates_to_jpeg()
templates: Template = Template.get_instance()
CTDT.initialize_template_cache()
config: Config = Config.get_instance()

print("Start Processing : {0}".format(datetime.now()))

####################################################################
# Solo = 11
if config.mode == 11:

    while True:
        Tsubasa.solo()
        time.sleep(config.sleep)
