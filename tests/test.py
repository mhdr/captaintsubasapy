from PIL import Image
import pytesseract
import cv2

# https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i
# https://github.com/UB-Mannheim/tesseract/wiki
# https://www.geeksforgeeks.org/python-string-isnumeric-application/
# https://stackoverflow.com/questions/19580102/inverting-image-in-python-with-opencv

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

image = cv2.imread("ocr.png")
gs_imagem = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

data = pytesseract.image_to_string(cv2.bitwise_not(gs_imagem))
new_data = ""

for d in data:
    if d.isnumeric():
        new_data += d

print(new_data)
