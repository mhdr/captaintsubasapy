import collections
import time
from datetime import datetime

import cv2
import pyautogui
from template import Template, TemplateProperties
from os import listdir
from os.path import isfile, join
from PIL import Image, ImageGrab
from openpyxl import Workbook, worksheet, load_workbook
import os
from PIL import Image
import numpy as np

Box = collections.namedtuple('Box', 'left top width height')


class LocateResult:
    template: TemplateProperties = None
    position: Box = None

    def __init__(self, temp: TemplateProperties = None, pos: Box = None):
        self.template = temp
        self.position = pos

    def click(self, wait: float = 5) -> bool:
        if self.position is not None:
            center_x = self.template.region_start_x + self.position.left + self.template.image_width / 2
            center_y = self.template.region_start_y + self.position.top + self.template.image_height / 2
            # pyautogui.moveTo(center_x, center_y)
            pyautogui.click(center_x, center_y)
            pyautogui.FAILSAFE = False
            pyautogui.moveTo(0, 0)
            print("Click Template => {0} : {1}".format(self.template.template_number, datetime.now()))
            time.sleep(wait)
            return True

        return False

    def move_mouse(self):
        if self.position is not None:
            center_x = self.template.region_start_x + self.position.left + self.template.image_width / 2
            center_y = self.template.region_start_y + self.position.top + self.template.image_height / 2
            pyautogui.moveTo(center_x, center_y)

    def available(self):
        if self.position is not None:
            return True

        return False


class LocateAllResult:
    positions = None

    def __init__(self, pos):
        self.positions = pos

    def click_center(self):
        pass

    def available(self):
        pass

    def count(self):
        pass


class CTDT:
    GRAYSCALE_DEFAULT = False

    @staticmethod
    def initialize_template_cache():
        tempalates = Template()
        dir = "templates"

        wb: Workbook = load_workbook(filename="data.xlsx")
        ws: worksheet = wb.active

        end_row = ws.max_row
        # start after header
        start_row = 2
        row_index = start_row

        while row_index <= end_row:
            template_number: str = str(ws["A" + str(row_index)].value)
            start_x = int(ws["B" + str(row_index)].value)
            start_y = int(ws["C" + str(row_index)].value)
            end_x = int(ws["D" + str(row_index)].value)
            end_y = int(ws["E" + str(row_index)].value)
            filename = join(dir, template_number + ".jpg")

            # Using 0 to read image in grayscale mode
            image = cv2.imread(filename, 0)
            width, height = image.shape[::-1]

            properties: TemplateProperties = TemplateProperties(template_number, image, width, height, start_x, start_y,
                                                                end_x, end_y)

            tempalates.cache[template_number] = properties

            row_index += 1

    @staticmethod
    def convert_templates_to_jpeg():
        src_dir = "templates_original"
        dest_dir = "templates"
        files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]

        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            image: Image.Image = Image.open(join(src_dir, file))
            # image_rgb = image.convert("RGB")
            image_rgb = image.convert("L")
            image_rgb.save(join(dest_dir, filename + ".jpg"), format='JPEG', quality=90)

    @staticmethod
    def click_location(x: int, y: int, clicks: int = 1, interval: float = 0, wait: float = 2):
        pyautogui.moveTo(x, y, 0.1)
        pyautogui.click(x, y, clicks=clicks, interval=interval)
        pyautogui.FAILSAFE = False
        pyautogui.moveTo(0, 0)
        time.sleep(wait)

    @staticmethod
    def locate_template(template_number: str, threshold=0.9) -> LocateResult:
        templates = Template()
        region_start_x = templates.cache[template_number].region_start_x
        region_start_y = templates.cache[template_number].region_start_y
        region_end_x = templates.cache[template_number].region_end_x
        region_end_y = templates.cache[template_number].region_end_y

        image_region = ImageGrab.grab(bbox=(region_start_x, region_start_y, region_end_x, region_end_y))
        image_template = templates.cache[template_number].image

        image_rgb = np.array(image_region)
        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(image_gray, image_template, cv2.TM_CCOEFF_NORMED)

        loc = np.where(res >= threshold)

        result: LocateResult = LocateResult()

        if len(loc[0]) == 0 & len(loc[1]) == 0:
            return result
        else:
            position = Box(loc[0][0], loc[1][0], templates.cache[template_number].image_width,
                           templates.cache[template_number].image_height)
            result = LocateResult(templates.cache[template_number], position)

        return result
