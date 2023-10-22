import math


class Referential:

    def __init__(self):
        self.x_src = None
        self.y_src = None
        self.x_dest = None
        self.y_dest = None

        self.dist_px_src_to_dest = None
        self.dist_mm_src_to_dest = None
        self.ratio_px_to_mm = None

        self.id_line_canvas = None

        self.is_defined = False

    def set_is_defined(self):
        self.is_defined = True

    def exists(self):
        return self.is_defined

    def get_id_line_canvas(self):
        return self.id_line_canvas

    def set_id_line_canvas(self, new_id):
        self.id_line_canvas = new_id

    def set_origin(self, x, y):
        self.x_src = x
        self.y_src = y

    def set_dest(self, x, y):
        self.x_dest = x
        self.y_dest = y

    def set_ratio_px_to_mm(self):
        self.ratio_px_to_mm = self.dist_mm_src_to_dest / self.dist_px_src_to_dest

    def get_ratio_px_to_mm(self):
        return self.ratio_px_to_mm

    def set_dist_mm_src_to_dest(self, dist_mm_input):
        self.dist_mm_src_to_dest = dist_mm_input

    def set_dist_px_src_to_dest(self):
        self.dist_px_src_to_dest = math.sqrt(
            math.pow(self.x_dest - self.x_src, 2) + math.pow(self.y_dest - self.x_dest, 2))

    def get_dist_px_src_to_dest(self):
        return self.dist_px_src_to_dest

    def get_dist_mm_src_to_dest(self):
        return self.dist_mm_src_to_dest

    def update_referential(self, x_dest, y_dest, dist_mm_input):
        self.set_dest(x_dest, y_dest)

        self.set_dist_px_src_to_dest()
        self.set_dist_mm_src_to_dest(dist_mm_input)

        self.set_ratio_px_to_mm()
        self.set_is_defined()

    def get_x_src(self):
        return self.x_src

    def get_y_src(self):
        return self.y_src

    def get_x_dest(self):
        return self.x_dest

    def get_y_dest(self):
        return self.y_dest

    def remove_from_canvas(self):
        to_delete_id_line = self.id_line_canvas
        self.set_id_line_canvas(None)
        return to_delete_id_line
