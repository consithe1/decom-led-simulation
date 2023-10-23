import math


class Referential(dict):

    def __init__(self):
        super().__init__()
        self["x_src"] = None
        self["y_src"] = None
        self["x_dest"] = None
        self["y_dest"] = None

        self["fill"] = "blue"
        self["dash"] = (10, 5)
        self["width"] = 2
        self["tags"] = "measuring"
        self["arrow"] = "both"

        self["dist_px_src_to_dest"] = 1000
        self["dist_mm_src_to_dest"] = 1000
        self["ratio_px_to_mm"] = 1

        self["id_line_canvas"] = None

    def set(self, key, val):
        self[key] = val

    def set_origin(self, x, y):
        self["x_src"] = x
        self["y_src"] = y

    def set_dest(self, x, y):
        self["x_dest"] = x
        self["y_dest"] = y

    def set_ratio_px_to_mm(self):
        self["ratio_px_to_mm"] = self["dist_mm_src_to_dest"] / self["dist_px_src_to_dest"]

    def set_dist_px_src_to_dest(self):
        self["dist_px_src_to_dest"] = math.sqrt(
            math.pow(self["x_dest"] - self["x_src"], 2) + math.pow(self["y_dest"] - self["x_dest"], 2))

    def update_referential(self, x_dest, y_dest, dist_mm_input):
        self.set_dest(x_dest, y_dest)

        self.set_dist_px_src_to_dest()
        self.set("dist_mm_src_to_dest", dist_mm_input)

        self.set_ratio_px_to_mm()

    def remove_from_canvas(self):
        to_delete_id_line = self["id_line_canvas"]
        self.set("id_line_canvas", None)
        return to_delete_id_line

    @staticmethod
    def from_json(dict_json: dict):
        ref = Referential()
        for key in dict_json.keys():
            ref.set(key, dict_json.get(key))
        return ref
