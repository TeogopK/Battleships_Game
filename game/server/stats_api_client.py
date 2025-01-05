import json
import requests
from game.libs.config_loader import load_config

config = load_config()


class StatsAPIClient:
    def __init__(self):
        self.base_url = config["api"]["base_url"]
        self.endpoint = config["api"]["endpoint"]
        self.full_url = f"{self.base_url}/{self.endpoint}"
        self.timeout = config["api"]["timeout"]

        self.team_0 = config["api"]["team_0"]
        self.team_1 = config["api"]["team_1"]

    def get_team_points(self, team_name):
        response = self._get_all_team_points()
        return response.get(team_name.lower(), None) if response else None

    def increment_team_points(self, team_name):
        team_boolean = 0 if team_name == self.team_0 else 1
        message = {"win": team_boolean}
        data_message = json.dumps(message)

        return self._post_increment_team_points(data_message)

    def _get_all_team_points(
        self,
    ):
        try:
            response = requests.get(self.full_url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during GET request: {e}")
            return None

    def _post_increment_team_points(self, data):
        try:
            response = requests.post(self.full_url, data=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during POST request: {e}")
            return None


def main():
    stats_api_client = StatsAPIClient()
    print(stats_api_client.get_team_points(stats_api_client.team_0))


main()
