import logging

from src.utils.referential import Referential
from src.rgb_leds.led_strip import LEDStrip
from src.utils.constants import *


class Parameters(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.logger.debug("Init Parameters object")

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

    def get_led_size_px(self):
        return self.led_size_px

    def set_led_size_px(self, value):
        self.led_size_px = value

    def get_image_src_path(self):
        return self.image_src_path

    def set_image_src_path(self, value):
        self.image_src_path = value

    def get_led_density(self):
        return self.led_density

    def set_led_density(self, value):
        self.led_density = value

    def get_simu_dest_path(self):
        return self.simu_dest_path

    def set_simu_dest_path(self, value):
        self.simu_dest_path = value

    def get_width(self):
        return self.width

    def set_width(self, value):
        self.width = value

    def get_app_mode(self):
        return self.app_mode

    def set_app_mode(self, value):
        self.app_mode = value

    def get_referential(self):
        return self.referential

    def set_referential(self, value):
        self.referential = value

    def get_description(self):
        return self.description

    def set_description(self, value):
        self.description = value

    def get_led_strips(self):
        return self.led_strips

    def set_led_strips(self, value):
        self.led_strips = value

    def get_next_strip_id(self):
        return self.next_strip_id

    def set_next_strip_id(self, value):
        self.next_strip_id = value

    def get_height(self):
        return self.height

    def set_height(self, value):
        self.height = value

    def add_led_strip(self, line_canvas):
        self.logger.debug("add_led_strip")
        self.led_strips.append(LEDStrip(line_canvas, self.next_strip_id))
        self.next_strip_id += 1

    def get_led_strip_at_index(self, index):
        return self.led_strips[index]

    def led_strips_pop(self):
        return self.led_strips.pop()

    def remove_referential_from_canvas(self):
        return self.referential.remove_from_canvas()


