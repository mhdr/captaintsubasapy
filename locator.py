from PIL import ImageGrab
import cv2
from lib import CTDT
import time
import os
import numpy as np

template_number = "020"
threshold = 0.9

time.sleep(5)
CTDT.convert_templates_to_jpeg()

image_screen = ImageGrab.grab()
image_template = cv2.imread(os.path.join("templates", template_number + ".jpg"), 0)
width, height = image_template.shape[::-1]

image_rgb = np.array(image_screen)
image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
res = cv2.matchTemplate(image_gray, image_template, cv2.TM_CCOEFF_NORMED)

loc = np.where(res >= threshold)

if len(loc[0]) == 0 & len(loc[1]) == 0:
    print("Not found")
else:
    start_y = loc[0][0]
    start_x = loc[1][0]

    end_x = start_x + width
    end_y = start_y + height

    print("Start X : {0}".format(start_x - 5))
    print("Start Y : {0}".format(start_y - 5))

    print("End X : {0}".format(end_x + 5))
    print("End Y : {0}".format(end_y + 5))
