class LED:

    def __init__(self, x=None, y=None, color='pink', led_size_px=2, id_led_canvas=None, id_strip=None, led_id=None,
                 led_id_from_strip=None, id_previous_led=None, id_next_led=None, manufacturer=None,
                 ic_per_led_active=None, ic_per_led_idle=None, input_voltage=None, waterproof_level=None,
                 led_width_mm=None, led_height_mm=None):
        self.manufacturer = manufacturer
        self.ic_per_led_active = ic_per_led_active
        self.ic_per_led_idle = ic_per_led_idle
        self.input_voltage = input_voltage
        self.waterproof_level = waterproof_level
        self.led_width_mm = led_width_mm
        self.led_height_mm = led_height_mm

        self.color = color
        self.led_size_px = led_size_px

        self.id_led_canvas = id_led_canvas

        self.id_strip = id_strip
        self.led_id_from_strip = led_id_from_strip

        self.led_id = led_id
        self.id_previous_led = id_previous_led
        self.id_next_led = id_next_led

        self.x = x
        self.y = y

    def get_ic_per_led_active(self):
        return self.ic_per_led_active

    def set_ic_per_led_active(self, value):
        self.ic_per_led_active = value

    def get_color(self):
        return self.color

    def set_color(self, value):
        self.color = value

    def get_id_strip(self):
        return self.id_strip

    def set_id_strip(self, value):
        self.id_strip = value

    def get_led_id(self):
        return self.led_id

    def set_led_id(self, value):
        self.led_id = value

    def get_id_previous_led(self):
        return self.id_previous_led

    def set_id_previous_led(self, value):
        self.id_previous_led = value

    def get_id_led_canvas(self):
        return self.id_led_canvas

    def set_id_led_canvas(self, value):
        self.id_led_canvas = value

    def get_id_next_led(self):
        return self.id_next_led

    def set_id_next_led(self, value):
        self.id_next_led = value

    def get_manufacturer(self):
        return self.manufacturer

    def set_manufacturer(self, value):
        self.manufacturer = value

    def get_led_size_px(self):
        return self.led_size_px

    def set_led_size_px(self, value):
        self.led_size_px = value

    def get_led_id_from_strip(self):
        return self.led_id_from_strip

    def set_led_id_from_strip(self, value):
        self.led_id_from_strip = value

    def get_x(self):
        return self.x

    def set_x(self, value):
        self.x = value

    def get_y(self):
        return self.y

    def set_y(self, value):
        self.y = value

    def get_waterproof_level(self):
        return self.waterproof_level

    def set_waterproof_level(self, value):
        self.waterproof_level = value

    def get_ic_per_led_idle(self):
        return self.ic_per_led_idle

    def set_ic_per_led_idle(self, value):
        self.ic_per_led_idle = value

    def get_led_height_mm(self):
        return self.led_height_mm

    def set_led_height_mm(self, value):
        self.led_height_mm = value

    def get_input_voltage(self):
        return self.input_voltage

    def set_input_voltage(self, value):
        self.input_voltage = value

    def get_led_width_mm(self):
        return self.led_width_mm

    def set_led_width_mm(self, value):
        self.led_width_mm = value

    def get_rect_coordinates(self):
        return int(self.get_x() - self.get_led_size_px() / 2), int(self.get_y() - self.get_led_size_px() / 2), int(
            self.get_x() + self.get_led_size_px() / 2), int(self.get_y() + self.get_led_size_px() / 2)


