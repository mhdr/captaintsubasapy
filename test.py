import pyscreeze
import time

time.sleep(5)

x = 748
y = 792
w = 232
h = 196

image_region = pyscreeze.screenshot('screenshot.png', region=(x, y, w, h))
print("Size : {0}, {1}".format(image_region.width, image_region.height))
image_template = pyscreeze.screenshot(region=(x - 5, y - 5, w + 5, h + 5))
pos = pyscreeze.locate(image_region, image_template, grayscale=True)
print(pos)
