import os
import sys
import time

print("Hello World")
time.sleep(3)

cmd = "python {0}".format(sys.argv[0])
# os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

os.system(cmd)
sys.exit()

time.sleep(10)
print("Hello World 2")
print("Hello World 3")
