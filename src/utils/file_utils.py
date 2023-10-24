import jsonpickle
import json
import logging

from src.utils.parameters import Parameters


class FileUtils:

    @staticmethod
    def save_simulation_to_file(parameters: Parameters):
        with open(parameters.get_simu_dest_path(), "w") as outfile:
            outfile.write(jsonpickle.encode(parameters, indent=4, keys=True))

    @staticmethod
    def read_simulation_from_file(filepath):
        with open(filepath, 'r') as readfile:
            reading = jsonpickle.decode(readfile.read(), keys=True)
            logging.debug(f"Import: {reading}")
            return reading
