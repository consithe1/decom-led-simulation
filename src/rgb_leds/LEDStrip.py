import math


class LEDStrip:

    def __init__(self, lines):
        self.lines = lines
        self.length = self.calculate_line_length()

    def calculate_line_length(self):
        d_total = 0
        for id_line, line in self.lines:
            x1, y1, x2, y2 = line
            d_total += math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        return int(d_total)
