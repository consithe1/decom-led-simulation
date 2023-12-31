import jsonpickle
import logging

from src.utils.parameters import Parameters


class FileUtils:
    logger = logging.getLogger(__name__)

    @staticmethod
    def save_simulation_to_file(parameters: Parameters):
        with open(parameters.get_simu_dest_path(), "w") as outfile:
            outfile.write(jsonpickle.encode(parameters, indent=4, keys=True))

    @staticmethod
    def read_simulation_from_file(filepath):
        with open(filepath, 'r') as readfile:
            return jsonpickle.decode(readfile.read(), keys=True)
