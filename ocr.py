import os

import cv2
import pytesseract
import numpy as np
from PIL import Image

from lib import CTDT, Cache

CTDT.initialize()
CTDT.initialize_cache()

template_number = "081"
invert_colors = True

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
caches: Cache = Cache.get_instance()
region_start_x = caches.templates[template_number].region_start_x
region_start_y = caches.templates[template_number].region_start_y
region_end_x = caches.templates[template_number].region_end_x
region_end_y = caches.templates[template_number].region_end_y

image_region = cv2.imread(os.path.join("templates_original", template_number + "f.png"))
image_region = image_region[region_start_y:region_end_y, region_start_x:region_end_x]

image_rgb = np.array(image_region)

image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
final_image = None

if invert_colors == True:
    final_image = cv2.bitwise_not(image_gray)  # color of text is white so we should invert colors
else:
    final_image = image_gray

data = pytesseract.image_to_string(final_image,config ='--psm 6')
print(data)

new_data = ""

for d in data:
    if d.isnumeric():
        new_data += d

if new_data == "":
    new_data = "0"

print(new_data)

cv2.imshow("test", final_image)
cv2.waitKey(0)
