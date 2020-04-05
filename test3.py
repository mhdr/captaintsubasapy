import ntpath
import os

filename = "templates_original/001.png"
print(ntpath.basename(filename))
print(os.path.basename(filename))
print(os.path.split(filename))
print(os.path.splitext(filename))
print(os.path.splitext(os.path.basename(filename)))
print(os.path.splitext(os.path.basename(filename))[0])
