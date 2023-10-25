import math
import logging


class Referential(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.logger.debug("Creating object")

        self.x_src = None
        self.y_src = None
        self.x_dest = None
        self.y_dest = None

        self.fill = "blue"
        self.dash = (10, 5)
        self.width = 2
        self.tags = "measuring"
        self.arrow = "both"

        self.dist_px_src_to_dest = 1000
        self.dist_mm_src_to_dest = 1000
        self.ratio_px_to_mm = 1

        self.id_line_canvas = None

    def get_arrow(self):
        return self.arrow

    def set_arrow(self, value):
        self.arrow = value

    def get_x_dest(self):
        return self.x_dest

    def set_x_dest(self, value):
        self.x_dest = value

    def get_y_src(self):
        return self.y_src

    def set_y_src(self, value):
        self.y_src = value

    def get_id_line_canvas(self):
        return self.id_line_canvas

    def set_id_line_canvas(self, value):
        self.id_line_canvas = value

    def get_y_dest(self):
        return self.y_dest

    def set_y_dest(self, value):
        self.y_dest = value

    def get_fill(self):
        return self.fill

    def set_fill(self, value):
        self.fill = value

    def get_tags(self):
        return self.tags

    def set_tags(self, value):
        self.tags = value

    def get_ratio_px_to_mm(self):
        return self.ratio_px_to_mm

    def get_width(self):
        return self.width

    def set_width(self, value):
        self.width = value

    def get_dist_px_src_to_dest(self):
        return self.dist_px_src_to_dest

    def get_x_src(self):
        return self.x_src

    def set_x_src(self, value):
        self.x_src = value

    def get_dash(self):
        return self.dash

    def set_dash(self, value):
        self.dash = value

    def get_dist_mm_src_to_dest(self):
        return self.dist_mm_src_to_dest

    def set_dist_mm_src_to_dest(self, value):
        self.dist_mm_src_to_dest = value

    def set_dest(self, x, y):
        self.x_dest = x
        self.y_dest = y

    def set_ratio_px_to_mm(self):
        self.ratio_px_to_mm = self.dist_mm_src_to_dest / self.dist_px_src_to_dest

    def set_dist_px_src_to_dest(self):
        self.dist_px_src_to_dest = math.sqrt(
            math.pow(self.get_x_dest() - self.get_x_src(), 2) + math.pow(self.get_y_dest() - self.get_x_dest(), 2))

    def update_referential(self, x_dest, y_dest, dist_mm_input):
        # update x et y dest
        self.set_x_dest(x_dest)
        self.set_y_dest(y_dest)

        self.update_referential_from_dist_mm(dist_mm_input)

    def update_referential_from_dist_mm(self, dist_mm_input):
        # update distance in px between src and dest
        self.set_dist_px_src_to_dest()
        # update distance in mm between src and dest
        self.set_dist_mm_src_to_dest(dist_mm_input)

        self.set_ratio_px_to_mm()

    def remove_from_canvas(self):
        to_delete_id_line = self.get_id_line_canvas()
        self.set_id_line_canvas(None)
        self.set_x_src(None)
        self.set_y_src(None)
        self.set_x_dest(None)
        self.set_y_dest(None)
        return to_delete_id_line
