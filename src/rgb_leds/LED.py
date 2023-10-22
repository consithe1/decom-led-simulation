
class LED:

    def __init__(self, coordinates):
        self.manufacturer = "Normand"
        self.ic_per_led_active = None
        self.ic_per_led_idle = None
        self.input_voltage = 12
        self.waterproof_level = "IP67"

        self.color = "pink"
        self.led_size_px = 8
        self.led_width_mm = 5.4
        self.led_height_mm = 5

        self.id_led_canvas = None

        self.x, self.y = coordinates

    def get_rect_coordinates(self):
        return int(self.x - self.led_size_px / 2), int(self.y - self.led_size_px / 2), int(self.x + self.led_size_px / 2), int(self.y + self.led_size_px / 2)
