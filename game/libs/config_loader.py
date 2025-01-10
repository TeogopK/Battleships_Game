import os
import sys
import yaml

_config = None

def load_config(file_path=None):
    global _config
    if _config is None:
        if file_path is None:
            if getattr(sys, 'frozen', False):
                # If running as a bundled app
                file_path = os.path.join(sys._MEIPASS, "config.yaml")
            else:
                # Normal execution (development mode)
                file_path = os.path.join(os.path.dirname(__file__), "../config.yaml")

        # Open and load the config
        with open(file_path, "r") as file:
            _config = yaml.safe_load(file)
    return _config
