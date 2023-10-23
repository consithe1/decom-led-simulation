from src.utils.referential import Referential
from src.rgb_leds.led_strip import LEDStrip
from src.utils.constants import *
import logging


class Parameters(dict):

    def __init__(self):
        super().__init__()
        self["led_density"] = 30
        self["app_mode"] = MEASURING
        self["led_size_px"] = 2
        self["referential"] = Referential()
        self["image_src_path"] = None
        self["simu_dest_path"] = None
        self["next_strip_id"] = 0

        self["description"] = ""
        self["led_strips"]: list[LEDStrip] = []

        self["width"] = 1600
        self["height"] = 800

    def from_json(self, dict_json: dict):
        for field in dict_json.keys():
            if field == "referential":
                logging.debug(f"Referential JSON object: {dict_json[field]}")
                self["referential"] = Referential.from_json(dict_json[field])
            elif field == "led_strips":
                self["led_strips"] = [LEDStrip.from_json(led_strip) for led_strip in dict_json[field]]
                logging.debug(f'LED Strips: {self["led_strips"]}')
            else:
                self[field] = dict_json[field]

    def add_led_strip(self, line_canvas):
        self["led_strips"].append(LEDStrip(line_canvas, self["next_strip_id"]))
        self["next_strip_id"] += 1

    def get_led_strip_at_index(self, index):
        return self.get("led_strips")[index]

    def get_led_strips(self):
        return self.get("led_strips")
