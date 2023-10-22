import math
from scipy import interpolate

class LEDStrip:

    def __init__(self, lines: list[int, list[int]]):
        self.length_px = None
        self.length_mm = None
        self.lines_canvas = lines
        self.list_leds = []
        self.calculate_line_length()

        self.spline_function = None

    def calculate_line_length(self):
        d_total = 0
        for _, line in self.lines_canvas:
            x1, y1, x2, y2 = line
            d_total += math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        self.length_px = int(d_total)

    def calculate_line_mm(self, reference):
        pass

    def add_led(self, led):
        self.list_leds.append(led)

    def delete_object(self):
        to_delete_ids = []
        for id_line, _ in self.lines_canvas:
            to_delete_ids.append(id_line)
        for led in self.list_leds:
            to_delete_ids.append(led.id_led_canvas)

        self.lines_canvas = []
        self.list_leds = []

        return to_delete_ids

    def generate_leds(self, dist_px_between_leds):
        self.generate_spline()

        # for each line associated with this strip in the canvas, add a LED to calculated coordinates with spline
        pass

    def generate_spline(self):
        x_points = []
        y_points = []
        for id_line, [x_src, y_src, x_dest, y_dest] in self.lines_canvas:
            x_points.append(x_src)
            x_points.append(x_dest)
            y_points.append(y_src)
            y_points.append(y_dest)
        self.spline_function = interpolate.splrep(x_points, y_points)

