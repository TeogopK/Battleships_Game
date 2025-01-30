"""Module for loading the config file."""

import os
import sys
import yaml

_CONFIG = None


def load_config(file_path=None):
    """Loads the config file and returns the config dictionary."""
    global _CONFIG  # pylint: disable=global-statement
    if _CONFIG is None:
        if file_path is None:
            if getattr(sys, "frozen", False):
                # If running as a bundled app
                file_path = os.path.join(sys._MEIPASS, "config.yaml")  # pylint: disable=protected-access
            else:
                # Normal execution (development mode)
                file_path = os.path.join(os.path.dirname(__file__), "../config.yaml")

        # Open and load the config
        with open(file_path, "r", encoding="utf-8") as file:
            _CONFIG = yaml.safe_load(file)
    return _CONFIG
