class LED:

    LED_ID = 0

    def __init__(self, coordinates=None, led_size_px=2, strip_id=0, led_id_from_strip=0):
        if coordinates is None:
            coordinates = [0, 0]
        self.manufacturer = "Normand"
        self.ic_per_led_active = None
        self.ic_per_led_idle = None
        self.input_voltage = 12
        self.waterproof_level = "IP67"

        self.color = "pink"
        self.led_size_px = led_size_px
        self.led_width_mm = 5.4
        self.led_height_mm = 5

        self.id_led_canvas = None

        self.id_strip = strip_id

        self.led_id = f"{self.id_strip}-{led_id_from_strip}"
        self.id_previous_led = None
        self.id_next_led = None

        self.x = coordinates[0]
        self.y = coordinates[1]

    def set_id_led_canvas(self, new_id):
        self.id_led_canvas = new_id

    def set_id_previous_led(self, pre):
        self.id_previous_led = pre

    def set_id_next_led(self, next_id):
        self.id_next_led = next_id

    def get_id_led(self):
        return self.led_id

    def get_rect_coordinates(self):
        return int(self.x - self.led_size_px / 2), int(self.y - self.led_size_px / 2), int(
            self.x + self.led_size_px / 2), int(self.y + self.led_size_px / 2)

    def to_json(self):
        dict_json = {}
        for field in vars(self).keys():
            dict_json[field] = getattr(self, field)
        return dict_json

    def from_json(self, dict_json: dict):
        for field in dict_json.keys():
            setattr(self, field, dict_json[field])
