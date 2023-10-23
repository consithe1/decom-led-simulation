class LED(dict):

    def __init__(self, x=None, y=None, color='pink', led_size_px=None, id_led_canvas=None, id_strip=None, led_id=None,
                 led_id_from_strip=None, id_previous_led=None, id_next_led=None, manufacturer=None,
                 ic_per_led_active=None, ic_per_led_idle=None, input_voltage=None, waterproof_level=None,
                 led_width_mm=None, led_height_mm=None):
        super().__init__()
        self["manufacturer"] = manufacturer
        self["ic_per_led_active"] = ic_per_led_active
        self["ic_per_led_idle"] = ic_per_led_idle
        self["input_voltage"] = input_voltage
        self["waterproof_level"] = waterproof_level
        self["led_width_mm"] = led_width_mm
        self["led_height_mm"] = led_height_mm

        self["color"] = color
        self["led_size_px"] = led_size_px

        self["id_led_canvas"] = id_led_canvas

        self["id_strip"] = id_strip
        self["led_id_from_strip"] = led_id_from_strip

        self["led_id"] = led_id
        self["id_previous_led"] = id_previous_led
        self["id_next_led"] = id_next_led

        self.x = x
        self.y = y

    def get_rect_coordinates(self):
        return int(self.x - self["led_size_px"] / 2), int(self.y - self["led_size_px"] / 2), int(
            self.x + self["led_size_px"] / 2), int(self.y + self["led_size_px"] / 2)

    def to_json(self):
        dict_json = {}
        for field in vars(self).keys():
            dict_json[field] = getattr(self, field)
        return dict_json

    @staticmethod
    def from_json(dict_json):
        led = LED()
        for key in dict_json.keys():
            led[key] = dict_json[key]
        return led

    def set(self, key, val):
        self[key] = val
