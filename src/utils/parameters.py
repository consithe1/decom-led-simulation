from src.utils.referential import Referential
from src.rgb_leds.led_strip import LEDStrip
from src.utils.constants import *
import json
import logging


class Parameters:

    def __init__(self):
        self.led_density = 30
        self.app_mode = MEASURING
        self.led_size_px = 2
        self.referential = Referential()
        self.image_src_path = None
        self.simu_dest_path = None
        self.next_strip_id = 0

        self.description = ""
        self.led_strips: list[LEDStrip] = []

        self.width = 1600
        self.height = 800

    def to_json(self):
        dict_json = {}
        for field in vars(self).keys():
            if field in ["referential", "led_strips"]:
                if type(getattr(self, field)) is list:
                    elem = [field_item.to_json() for field_item in getattr(self, field)]
                else:
                    elem = getattr(self, field).to_json()
                dict_json[field] = elem
            else:
                dict_json[field] = getattr(self, field)

        return json.dumps(dict_json, sort_keys=True, indent=4)

    def from_json(self, dict_json: dict):
        for field in dict_json.keys():
            if field == "referential":
                logging.debug(f"Referential JSON object: {dict_json[field]}")
                self.referential.from_json(dict_json[field])
            elif field == "led_strips":
                for led_strip in dict_json[field]:
                    logging.debug(f"LEDStrip JSON object: {led_strip}")
                    l_strip = LEDStrip().from_json(led_strip)
                    self.led_strips.append(l_strip)
            else:
                setattr(self, field, dict_json[field])

    def add_led_strip(self, line_canvas):
        self.led_strips.append(LEDStrip(line_canvas, self.next_strip_id))
        self.next_strip_id += 1
