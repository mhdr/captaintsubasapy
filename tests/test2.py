# Our convertion from millimeters to inches
MM_TO_IN = 0.0393700787

# Import the libraries
import ctypes
import tkinter

# Set process DPI awareness
ctypes.windll.shcore.SetProcessDpiAwareness(1)
# Create a tkinter window
root = tkinter.Tk()
# Get a DC from the window's HWND
dc = ctypes.windll.user32.GetDC(root.winfo_id())
# The the monitor phyical width
# (returned in millimeters then converted to inches)
mw = ctypes.windll.gdi32.GetDeviceCaps(dc, 4) * MM_TO_IN
# The the monitor phyical height
mh = ctypes.windll.gdi32.GetDeviceCaps(dc, 6) * MM_TO_IN
# Get the monitor horizontal resolution
dw = ctypes.windll.gdi32.GetDeviceCaps(dc, 8)
# Get the monitor vertical resolution
dh = ctypes.windll.gdi32.GetDeviceCaps(dc, 10)
# Destroy the window
root.destroy()

# Horizontal and vertical DPIs calculated
hdpi, vdpi = dw / mw, dh / mh
# Diagonal DPI calculated using Pythagoras
ddpi = (dw ** 2 + dh ** 2) ** 0.5 / (mw ** 2 + mh ** 2) ** 0.5
# Print the DPIs
print(round(hdpi, 1), round(vdpi, 1), round(ddpi, 1))