"""This module contains the StatsAPIClient class responsible for interacting with the stats API."""

import json
import requests
from game.libs.config_loader import load_config

config = load_config()


class StatsAPIClient:
    """A client for interacting with the stats API to retrieve and update team points."""

    def __init__(self):
        """Initializes the StatsAPIClient instance with the API base URL, endpoint, and timeout."""
        self.base_url = config["api"]["base_url"]
        self.endpoint = config["api"]["endpoint"]
        self.full_url = f"{self.base_url}/{self.endpoint}"
        self.timeout = config["api"]["timeout"]

        self.team_0 = config["api"]["team_0"]
        self.team_1 = config["api"]["team_1"]

    def get_team_points(self, team_name):
        """Retrieves the points for the specified team from the stats API.

        Args:
            team_name (str): The name of the team to retrieve points for.
        """
        response = self._get_all_team_points()
        return response.get(team_name.lower(), None) if response is not None else None

    def increment_team_points(self, team_name):
        """Increments the points for the specified team in the stats API.

        Args:
            team_name (str): The name of the team to increment points for.
        """
        if team_name is None:
            print("No intial team for winner")
            return None

        team_boolean = 0 if team_name == self.team_0 else 1
        message = {"win": team_boolean}
        data_message = json.dumps(message)

        return self._post_increment_team_points(data_message)

    def _get_all_team_points(
        self,
    ):
        """Retrieves the team points for each team from the stats API."""
        try:
            response = requests.get(self.full_url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as request_exception:  # pylint: disable=W0703
            print(f"Error during GET request: {request_exception}")
            return None

    def _post_increment_team_points(self, data):
        """
        Increments the points for the specified team as JSON data 0 or 1 in the stats API.
        """
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(self.full_url, data=data, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as request_exception:  # pylint: disable=W0703
            print(f"Error during POST request: {request_exception}")
            return None
