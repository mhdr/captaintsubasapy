import base64
import os
import subprocess
from time import time

import cv2
import numpy as np

start_time = time()

pipe = subprocess.Popen('"C:\\Program Files\\Nox\\bin\\nox_adb.exe" exec-out screencap -p', stdout=subprocess.PIPE, shell=True)
img_bytes = pipe.stdout.read()
read_time = time()

img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
end_time = time()

print('stream size', len(img_bytes))
print('read', read_time - start_time)
print('decode', end_time - read_time)
print('screencap', end_time - start_time)

cv2.imshow("", img)
cv2.waitKey(0)
cv2.destroyWindow("")
cv2.imwrite("screen2.jpg",img)