import yaml
import os

_config = None


def load_config(file_path=None):
    global _config
    if _config is None:
        # Determine default path relative to the current file
        if file_path is None:
            file_path = os.path.join(os.path.dirname(__file__), "../config.yaml")

        # Open and load the config
        with open(file_path, "r") as file:
            _config = yaml.safe_load(file)
    return _config
