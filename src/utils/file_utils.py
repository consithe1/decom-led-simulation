import json

from src.utils.parameters import Parameters


class FileUtils:

    @staticmethod
    def save_simulation_to_file(parameters: Parameters):
        with open(parameters.get("simu_dest_path"), "w") as outfile:
            outfile.write(json.dumps(parameters, indent=4))

    @staticmethod
    def read_simulation_from_file(filepath):
        with open(filepath, 'r') as readfile:
            return json.load(readfile)
