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

    def __init__(self, lines=None):
        if lines is None:
            lines = []
        self.length_px = None
        self.length_mm = None
        self.led_density = None
        self.lines_canvas: list = lines
        self.list_leds: list[LED] = []

    def calculate_line_mm(self, reference):
        pass

    def calculate_number_leds(self):
        return len(self.list_leds)

    def get_list_leds(self):
        return self.list_leds

    def add_led(self, led):
        self.list_leds.append(led)

    def add_lines(self, list_elem):
        self.lines_canvas = list_elem

    def remove_leds(self):
        to_delete_ids = []
        for led in self.list_leds:
            to_delete_ids.append(led.id_led_canvas)

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

    def generate_path_between_canvas_lines(self):
        # ratio_px_to_mm -> 1 px = x mm

        full_path = []
        for id_obj, [x_src, y_src, x_dest, y_dest] in self.lines_canvas:
            tmp_path_v2 = generate_path_between_coordinates_v2(x_src, y_src, x_dest, y_dest)
            full_path.extend(tmp_path_v2)

        return full_path

    def add_id_canvas_to_led(self, index, new_id):
        self.list_leds[index].set_id_led_canvas(new_id)

    def add_prev_id_canvas_to_led(self, index, prev_id):
        self.list_leds[index].set_id_previous_led_canvas(prev_id)

    def add_next_id_canvas_to_led(self, index, next_id):
        self.list_leds[index].set_id_next_led_canvas(next_id)

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
                led = LED((x, y), led_size)
                self.list_leds.append(led)

            travel_distance += 1

    def to_json(self):
        dict_json = {}
        for field in vars(self).keys():
            if field in ["list_leds"]:
                if type(getattr(self, field)) is list:
                    elem = [field_item.to_json() for field_item in getattr(self, field)]
                else:
                    elem = getattr(self, field).to_json()
                dict_json[field] = elem
            else:
                dict_json[field] = getattr(self, field)
        return dict_json

    def from_json(self, dict_json):
        for field in dict_json.keys():
            if field == "lines_canvas":
                self.lines_canvas = [line_canvas for line_canvas in dict_json[field]]

            elif field == "list_leds":
                for led_json in dict_json[field]:
                    led = LED()
                    led.from_json(led_json)
                    self.list_leds.append(led)
            else:
                setattr(self, field, dict_json[field])

        print("LED strip:", vars(self))
