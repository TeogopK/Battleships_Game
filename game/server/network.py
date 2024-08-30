import socket
from abc import ABC, abstractmethod


class AbstractNetwork(ABC):
    @abstractmethod
    def send(self, data):
        pass

    @abstractmethod
    def close(self):
        pass


class OfflineNetwork(AbstractNetwork):
    def __init__(self, is_player=True):
        self.is_player = is_player
        self.server_instance = None

    def add_server_instance(self, server_instance):
        self.server_instance = server_instance

    def send(self, data):
        """Simulate sending data to the server and receiving a response."""
        response = self.server_instance.handle_offline_client(data, is_player=self.is_player)
        return response

    def close(self):
        """Offline mode does not require cleanup."""


class MultiplayerNetwork(AbstractNetwork):
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()
        print("Connected to server!")

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.settimeout(10)
            return self.client.recv(2048).decode()
        except socket.timeout as exception:
            raise ConnectionError("Connection timed out while trying to receive initial data.") from exception
        except socket.error as exception:
            raise ConnectionError(f"Socket error: {exception}") from exception

    def send(self, data):
        try:
            print(data)
            self.client.send(str.encode(data))
            self.client.settimeout(60)
            response = self.client.recv(2048).decode()
            return response
        except socket.timeout:
            print("Socket timed out while waiting for a response.")
        except socket.error as exception:
            print(f"Socket error: {exception}")
        return None

    def close(self):
        try:
            self.client.close()
        except socket.error as exception:
            print(f"Socket error during close: {exception}")
