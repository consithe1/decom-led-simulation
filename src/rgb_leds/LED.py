
class LED:

    def __init__(self, coordinates):
        self.manufacturer = None
        self.input_current = None
        self.input_voltage = None
        self.waterproof_level = None

        self.color = "pink"
        self.led_size = 8

        self.id_led_canvas = None

        self.x, self.y = coordinates

    def get_rect_coordinates(self):
        return int(self.x - self.led_size/2), int(self.y - self.led_size/2), int(self.x + self.led_size/2), int(self.y + self.led_size/2)
