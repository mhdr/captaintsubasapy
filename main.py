from pyscreeze import Box

from lib import CTDT
from template import Template
import time

time.sleep(5)

CTDT.convert_templates_to_jpeg()
templates = Template()
CTDT.initialize_template_cache()
result = CTDT.locate_template("001")
print(result.position)
result.click()
