from dataclasses import dataclass
from typing import Dict, List

import pyautogui
from PIL.Image import Image
from pyscreeze import Box


@dataclass()
class TemplateProperties:
    template_number: str
    image: Image
    image_width: int
    image_height: int
    region_start_x: int
    region_start_y: int
    region_end_x: int
    region_end_y: int


class Template:
    __instance = None
    cache: Dict[str, TemplateProperties] = {}

    @staticmethod
    def get_instance():
        """
        static access method
        :return: Template
        """
        if Template.__instance is None:
            Template()

        return Template.__instance

    def __init__(self):
        """
        Virtually private constructor
        """
        Template.__instance = self
