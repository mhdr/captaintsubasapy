import atexit
import time


def exit_handler():
    print('My application is ending!')


atexit.register(exit_handler)

while True:
    print("Run")
    time.sleep(1)