from PIL import ImageGrab
import cv2
from lib import CTDT
import time
import os
import numpy as np

threshold = 0.97
index = 7
# first match =0
match = 1

# Window name in which image is displayed
window_name = 'Image'

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

    start_x = loc[1][match]
    start_y = loc[0][match]

    end_x = start_x + width
    end_y = start_y + height

    print("Start X : {0}".format(start_x - 5))
    print("Start Y : {0}".format(start_y - 5))

    print("End X : {0}".format(end_x + 5))
    print("End Y : {0}".format(end_y + 5))

    print("Width : {0}".format(end_x - start_x))
    print("Height : {0}".format(end_y - start_y))

    start_point = (start_x, start_y)
    end_point = (end_x, end_y)

    # Red color in BGR
    color = (0, 0, 255)

    # Line thickness of 2 px
    thickness = 5

    # Using cv2.rectangle() method
    # Draw a rectangle with blue line borders of thickness of 2 px
    image = cv2.rectangle(image_screen, start_point, end_point, color, thickness)

    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    # Displaying the image
    cv2.imshow(window_name, image)

    k = cv2.waitKey(0)  # 0==wait forever
