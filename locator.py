from PIL import ImageGrab
import cv2
from lib import CTDT
import time
import os
import numpy as np

threshold = 0.9
index=31

template_number = "{0}".format(str(index).zfill(3))

image_screen = cv2.imread(os.path.join("templates_original", template_number + "f.png"))
image_template = cv2.imread(os.path.join("templates_original", template_number + ".png"), 0)
width, height = image_template.shape[::-1]

image_rgb = np.array(image_screen)
image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
res = cv2.matchTemplate(image_gray, image_template, cv2.TM_CCOEFF_NORMED)

loc = np.where(res >= threshold)

if len(loc[0]) == 0 & len(loc[1]) == 0:
    print("Not found")
else:

    start_x = loc[1][0]
    start_y = loc[0][0]

    end_x = start_x + width
    end_y = start_y + height

    print("Start X : {0}".format(start_x - 5))
    print("Start Y : {0}".format(start_y - 5))

    print("End X : {0}".format(end_x + 5))
    print("End Y : {0}".format(end_y + 5))
