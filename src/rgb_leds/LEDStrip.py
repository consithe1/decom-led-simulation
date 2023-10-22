import math
from scipy.interpolate import splprep, splev
import matplotlib.pyplot as plt
import numpy as np


class LEDStrip:

    def __init__(self, lines):
        self.spline_lines = []
        self.yp: np.ndarray
        self.xp: np.ndarray
        self.spline_u = None
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

    def get_spline_coordinates(self):
        return self.spline_lines

    def add_led(self, led):
        self.list_leds.append(led)

    def add_lines(self, list_elem):
        self.lines_canvas = list_elem

    def delete_object(self):
        to_delete_ids = []
        for id_line, _ in self.lines_canvas:
            to_delete_ids.append(id_line)
        for led in self.list_leds:
            to_delete_ids.append(led.id_led_canvas)

        self.lines_canvas = []
        self.list_leds = []

        return to_delete_ids

    def plot_spline(self):
        out = splev(self.spline_u, self.spline_function)
        plt.figure()
        plt.plot(out[0], out[1], 'g')
        plt.gca().invert_yaxis()
        plt.show()

    def generate_spline(self):
        x_points = []
        y_points = []
        old_lines_id = []

        print("Line canvas:", self.lines_canvas)

        for id_line, [x_src, y_src, x_dest, y_dest] in self.lines_canvas:
            x_points.append(x_src)
            x_points.append(x_dest)
            y_points.append(y_src)
            y_points.append(y_dest)
            old_lines_id.append(id_line)

        xp = np.array(x_points)
        yp = np.array(y_points)
        okay = np.where(np.abs(np.diff(xp)) + np.abs(np.diff(yp)) > 0)
        self.xp = np.r_[xp[okay], xp[-1]]
        self.yp = np.r_[yp[okay], yp[-1]]

        self.spline_function, self.spline_u = splprep([self.xp, self.yp], s=0)

        print(f"# init points: {len(x_points)} vs # final points: {np.prod(self.xp.shape)}")
        spline_x = list(self.xp)
        spline_y = list(self.yp)
        self.spline_lines = []
        for i in range(len(spline_x) - 1):
            self.spline_lines.append([spline_x[i], spline_y[i], spline_x[i + 1], spline_y[i + 1]])
