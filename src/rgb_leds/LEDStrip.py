import math


class LEDStrip:

    def __init__(self, lines):
        self.length_pixel = None
        self.length_mm = None
        self.lines = lines
        self.calculate_line_length()

    def calculate_line_length(self):
        d_total = 0
        for _, line in self.lines:
            x1, y1, x2, y2 = line
            d_total += math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        self.length_pixel = int(d_total)

    def calculate_line_mm(self, reference):
        pass

