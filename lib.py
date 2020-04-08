import collections
import time
from datetime import datetime
import cv2
import pyautogui
from os import listdir
from os.path import isfile, join
from PIL import Image, ImageGrab
from openpyxl import Workbook, worksheet, load_workbook
import os
from PIL import Image
import numpy as np
from dataclasses import dataclass
from typing import Dict, List
import datetime
import configparser

#######################################################################################################################

Box = collections.namedtuple('Box', 'left top width height')


#######################################################################################################################

@dataclass()
class TemplateProperties:
    template_number: str
    image: any
    image_width: int
    image_height: int
    region_start_x: int
    region_start_y: int
    region_end_x: int
    region_end_y: int
    date_seen: datetime.datetime


#######################################################################################################################

@dataclass()
class LocationProperties:
    location_number: str
    x: int
    y: int


#######################################################################################################################

class Cache:
    __instance = None
    templates: Dict[str, TemplateProperties] = {}
    locations: Dict[str, LocationProperties] = {}

    @staticmethod
    def get_instance():
        """
        static access method
        :return: Template
        """
        if Cache.__instance is None:
            Cache()

        return Cache.__instance

    def __init__(self):
        """
        Virtually private constructor
        """
        Cache.__instance = self


#######################################################################################################################

class Config:
    __instance = None
    mode: int
    sleep: float
    energy_recovery: int
    wait_energy_recovery: int

    telegram_token: str
    telegram_chatid: int
    telegram_disabled: int

    @staticmethod
    def get_instance():
        """
        static access method
        :return: Template
        """
        if Config.__instance is None:
            config = configparser.ConfigParser()
            config.read('config.ini')

            Config.mode = int(config["Game"]["Mode"])
            Config.sleep = float(config["General"]["Sleep"])

            Config.energy_recovery = int(config["Game"]["EnergyRecovery"])
            Config.wait_energy_recovery = int(config["Game"]["WaitForEnergyRecovery"])

            Config.telegram_token = str(config["Telegram"]["Token"])
            Config.telegram_chatid = int(config["Telegram"]["86168181"])
            Config.telegram_disabled = int(config["Telegram"]["Disabled"])

            Config()

        return Config.__instance

    def __init__(self):
        """
        Virtually private constructor
        """
        Config.__instance = self


#######################################################################################################################

class LocateResult:
    template: TemplateProperties = None
    position: Box = None

    def __init__(self, temp: TemplateProperties = None, pos: Box = None):
        self.template = temp
        self.position = pos

    def click(self, wait: float = 2) -> bool:
        if self.position is not None:
            center_x = self.template.region_start_x + self.position.left + self.template.image_width / 2
            center_y = self.template.region_start_y + self.position.top + self.template.image_height / 2
            # pyautogui.moveTo(center_x, center_y)
            pyautogui.click(center_x, center_y)
            pyautogui.FAILSAFE = False
            pyautogui.moveTo(0, 0)
            print("Click Template => {0} : {1}".format(self.template.template_number, datetime.datetime.now()))
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


#######################################################################################################################

class CTDT:

    @staticmethod
    def initialize_cache():
        caches: Cache = Cache.get_instance()
        dir = "templates"

        wb: Workbook = load_workbook(filename="data.xlsx")
        ws: worksheet = wb["Sheet1"]
        ws2: worksheet = wb["Sheet2"]

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

            template_properties: TemplateProperties = TemplateProperties(template_number, image, width, height, start_x,
                                                                         start_y,
                                                                         end_x, end_y, None)

            caches.templates[template_number] = template_properties
            row_index += 1

        end_row2 = ws2.max_row
        start_row2 = 2
        row_index2 = start_row2

        while row_index2 <= end_row2:
            location_number: str = str(ws2["A" + str(row_index2)].value)
            x: int = int(ws2["B" + str(row_index2)].value)
            y: int = int(ws2["C" + str(row_index2)].value)

            location_properties = LocationProperties(location_number, x, y)

            caches.locations[location_number] = location_properties
            row_index2 += 1

    @staticmethod
    def convert_templates_to_jpeg():
        dest_dir = "templates"
        src_dir = "templates_original"

        files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]

        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]

            if filename.endswith("f"):
                continue

            image: Image.Image = Image.open(join(src_dir, file))
            # image_rgb = image.convert("RGB")
            image_rgb = image.convert("L")
            image_rgb.save(join(dest_dir, filename + ".jpg"), format='JPEG', quality=90)

    @staticmethod
    def click_location(location_number: str, clicks: int = 1, interval: float = 0, wait: float = 2):
        caches: Cache = Cache.get_instance()
        x = caches.locations[location_number].x
        y = caches.locations[location_number].y
        pyautogui.moveTo(x, y, 0.1)
        pyautogui.click(x, y, clicks=clicks, interval=interval)
        pyautogui.FAILSAFE = False
        pyautogui.moveTo(0, 0)
        time.sleep(wait)

    @staticmethod
    def locate_template(template_number: str, threshold=0.9) -> LocateResult:
        caches: Cache = Cache.get_instance()
        region_start_x = caches.templates[template_number].region_start_x
        region_start_y = caches.templates[template_number].region_start_y
        region_end_x = caches.templates[template_number].region_end_x
        region_end_y = caches.templates[template_number].region_end_y

        image_region = ImageGrab.grab(bbox=(region_start_x, region_start_y, region_end_x, region_end_y))
        image_template = caches.templates[template_number].image

        image_rgb = np.array(image_region)
        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(image_gray, image_template, cv2.TM_CCOEFF_NORMED)

        loc = np.where(res >= threshold)

        result: LocateResult = LocateResult()

        if len(loc[0]) == 0 & len(loc[1]) == 0:
            return result
        else:
            position = Box(loc[0][0], loc[1][0], caches.templates[template_number].image_width,
                           caches.templates[template_number].image_height)
            result = LocateResult(caches.templates[template_number], position)
            caches.templates[template_number].date_seen = datetime.datetime.now()

        return result
