from src.utils.parameters import Parameters
from src.utils.constants import *
import json


class FileUtils:

    @staticmethod
    def save_simulation_to_file(parameters: Parameters):
        with open(parameters.simu_dest_path, "w") as outfile:
            outfile.write(parameters.to_json())

    @staticmethod
    def read_simulation_from_file(filepath):
        with open(filepath, 'r') as readfile:
            return json.load(readfile)
