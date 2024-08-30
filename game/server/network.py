"""
Network communication module.

This module defines abstract and concrete classes for network communication,
including offline simulation and real multiplayer networking.
"""

import socket
from abc import ABC, abstractmethod


class AbstractNetwork(ABC):
    """
    Abstract base class for network communication.

    Defines the basic interface for sending data and closing the connection.
    """

    @abstractmethod
    def send(self, data):
        """
        Sends data through the network.

        Args:
            data (str): The data to send.

        Returns:
            str: The response received after sending the data.
        """

    @abstractmethod
    def close(self):
        """
        Closes the network connection.
        """


class OfflineNetwork(AbstractNetwork):
    """
    Simulates network communication for offline scenarios.

    This class is used for testing or offline use where no real network communication
    is needed.
    """

    def __init__(self, is_player=True):
        """
        Initializes an OfflineNetwork instance.

        Args:
            is_player (bool): Indicates if the network instance is for a player. Defaults to True.
        """
        self.is_player = is_player
        self.server_instance = None

    def add_server_instance(self, server_instance):
        """
        Sets the server instance for offline communication.

        Args:
            server_instance (Server): The server instance to handle offline client data.
        """
        self.server_instance = server_instance

    def send(self, data):
        """
        Simulates sending data to the server and receiving a response.

        Args:
            data (str): The data to send.

        Returns:
            str: The simulated response from the server.
        """
        response = self.server_instance.handle_offline_client(data, is_player=self.is_player)
        return response

    def close(self):
        """
        Offline mode does not require cleanup.
        """


class MultiplayerNetwork(AbstractNetwork):
    """
    Handles network communication for multiplayer scenarios using real sockets.

    Connects to a server, sends data, and receives responses over a TCP connection.
    """

    def __init__(self):
        """
        Initializes a MultiplayerNetwork instance and connects to the server.
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()
        print("Connected to server!")

    def connect(self):
        """
        Connects to the server and handles initial communication.

        Raises:
            ConnectionError: If the connection times out or encounters a socket error.
        """
        try:
            self.client.connect(self.addr)
            self.client.settimeout(10)
            return self.client.recv(2048).decode()
        except socket.timeout as exception:
            raise ConnectionError("Connection timed out while trying to receive initial data.") from exception
        except socket.error as exception:
            raise ConnectionError(f"Socket error: {exception}") from exception

    def send(self, data):
        """
        Sends data to the server and waits for a response.

        Args:
            data (str): The data to send.

        Returns:
            str: The response received from the server, or None if an error occurs.
        """
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
        """
        Closes the socket connection to the server.

        Raises:
            socket.error: If a socket error occurs during the closing process.
        """
        try:
            self.client.close()
        except socket.error as exception:
            print(f"Socket error during close: {exception}")
