from dataclasses import dataclass
from typing import Dict, List


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


@dataclass()
class LocationProperties:
    location_number: str
    x: int
    y: int


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
