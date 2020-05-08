import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

image = cv2.imread("ocr.png")
image_grayscal = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
inverted_image = cv2.bitwise_not(image_grayscal) # color of text is white so we should invert colors

data = pytesseract.image_to_string(inverted_image)
new_data = ""

for d in data:
    if d.isnumeric():
        new_data += d

print(new_data)



# https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i
# https://github.com/UB-Mannheim/tesseract/wiki
