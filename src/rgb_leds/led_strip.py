import math

from src.rgb_leds.led import LED


def generate_path_between_coordinates_v2(x_src, y_src, x_dest, y_dest):
    x_next, y_next = x_src, y_src
    path = []
    pos_i = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    while x_next != x_dest or y_next != y_dest:
        path.append([x_next, y_next])
        # calculate the direction of destination
        min_dist = math.inf
        x_candidate, y_candidate = x_next, y_next
        for x_i, y_i in pos_i:
            x_tmp, y_tmp = x_next + x_i, y_next + y_i
            dist_tmp = calculate_line_length(x_tmp, y_tmp, x_dest, y_dest)

            if dist_tmp < min_dist:
                min_dist = dist_tmp
                x_candidate, y_candidate = x_tmp, y_tmp

        x_next, y_next = x_candidate, y_candidate

    return path


def calculate_line_length(x_src, y_src, x_dest, y_dest):
    return math.sqrt(math.pow(y_dest - y_src, 2) + math.pow(x_dest - x_src, 2))


class LEDStrip:

    def __init__(self, lines=None, next_strip_id=0):
        if lines is None:
            lines = []

        self.length_px = None
        self.length_mm = None
        self.led_density = None
        self.lines_canvas: list[list[int, list[int]]] = lines
        self.list_leds: list[LED] = []

        self.fill = "red"
        self.width = 1

        self.strip_id = next_strip_id
        self.next_led_id = 0

    def get_list_leds(self):
        return self.list_leds

    def set_list_leds(self, value):
        self.list_leds = value

    def get_length_mm(self):
        return self.length_mm

    def set_length_mm(self, value):
        self.length_mm = value

    def get_lines_canvas(self):
        return self.lines_canvas

    def set_lines_canvas(self, value):
        self.lines_canvas = value

    def get_length_px(self):
        return self.length_px

    def set_length_px(self, value):
        self.length_px = value

    def get_led_density(self):
        return self.led_density

    def set_led_density(self, value):
        self.led_density = value

    def get_width(self):
        return self.width

    def set_width(self, value):
        self.width = value

    def get_fill(self):
        return self.fill

    def set_fill(self, value):
        self.fill = value

    def get_strip_id(self):
        return self.strip_id

    def set_strip_id(self, value):
        self.strip_id = value

    def get_next_led_id(self):
        return self.next_led_id

    def set_next_led_id(self, value):
        self.next_led_id = value

    def calculate_line_mm(self, reference):
        pass

    def calculate_number_leds(self):
        return len(self.list_leds)

    def remove_leds(self):
        to_delete_ids = []
        for led in self.list_leds:
            to_delete_ids.append(led.get_id_led_canvas())

        self.list_leds = []
        return to_delete_ids

    def delete_object(self):
        to_delete_ids = []
        for id_line, _ in self.lines_canvas:
            to_delete_ids.append(id_line)

        to_delete_ids.extend(self.remove_leds())

        self.lines_canvas = []
        self.list_leds = []

        return to_delete_ids

    def update_id_led_canvas_at_index(self, index_led, new_led_id):
        self.list_leds[index_led].set_id_led_canvas(new_led_id)

    def generate_path_between_canvas_lines(self):
        # ratio_px_to_mm -> 1 px = x mm

        full_path = []
        for id_obj, [x_src, y_src, x_dest, y_dest] in self.lines_canvas:
            tmp_path_v2 = generate_path_between_coordinates_v2(x_src, y_src, x_dest, y_dest)
            full_path.extend(tmp_path_v2)

        return full_path

    def add_prev_id_to_led(self, index, prev_id):
        self.list_leds[index].set_id_previous_led(prev_id)

    def add_next_id_to_led(self, index, next_id):
        self.list_leds[index].set_id_next_led(next_id)

    def get_id_led_at_index(self, index):
        return self.list_leds[index].get_led_id()

    def get_led_at_index(self, index):
        return self.list_leds[index]

    def calculate_led_positions(self, ratio_px_to_mm, density, led_size):
        path = self.generate_path_between_canvas_lines()

        # define distance between leds in px
        d_px = int((1000 / density) * (1 / ratio_px_to_mm))

        # follow path and increment each time
        travel_distance = d_px
        for x, y in path:

            if travel_distance >= d_px:
                travel_distance = -1

                # add led or position
                self.add_new_led(x, y, led_size)

            travel_distance += 1

    def add_new_led(self, x, y, led_size):
        self.list_leds.append(LED(x=x, y=y, led_size_px=led_size, color='pink', id_strip=self.get_strip_id(),
                                  led_id_from_strip=self.get_next_led_id(),
                                  led_id=f'{self.get_strip_id()}-{self.get_next_led_id()}'))
        self.next_led_id += 1
