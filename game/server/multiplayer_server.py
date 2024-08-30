"""Module that creates a server for managing multiplayer game sessions with network communication."""

import socket
from _thread import start_new_thread
from game.server.game_server import GameServer


class MultiplayerServer(GameServer):
    """
    A server for managing multiplayer game sessions with network communication.

    Inherits from GameServer and provides networking capabilities for handling client connections
    and communication using sockets.
    """

    TIME_PER_TURN = 60

    def __init__(self):
        """
        Initializes the MultiplayerServer instance and sets up the server socket.

        Configures the server to listen for incoming client connections on a specified address and port.
        """
        super().__init__(self.TIME_PER_TURN)
        self.server = "localhost"
        self.port = 5555
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setup_server()

    def setup_server(self):
        """
        Configures the server socket to bind to the specified address and port,
        and starts listening for incoming connections.

        Raises:
            Exception: If there is an error during socket setup, the socket is closed and the exception is raised.
        """
        try:
            self.server_socket.bind((self.server, self.port))
            self.server_socket.listen(5)
            print(f"Server started, listening on {self.server}:{self.port}")
        except socket.error as exception:
            print(f"Socket error during setup: {exception}")
            self.server_socket.close()
            raise

    def run(self):
        """
        Main loop for accepting client connections and handling them in separate threads.

        Continuously accepts new client connections and starts a new thread to handle each client.
        """
        while True:
            try:
                conn, addr = self.server_socket.accept()
                print(f"Connected to: {addr}")
                start_new_thread(self._handle_client, (conn,))
            except Exception as exception:  # pylint: disable=W0703
                print(f"Exception in accepting connections: {exception}")

    def _handle_client(self, conn):
        """
        Handles communication with a connected client.

        Receives commands from the client, processes them using the command handler, and sends responses back.

        Args:
            conn (socket.socket): The socket object for the connected client.
        """
        conn.send(str.encode("Connected"))
        while True:
            try:
                data = conn.recv(2048)
                if not data:
                    print("Client disconnected")
                    break

                command = data.decode("utf-8")
                response = self.command_handler.handle_command(command, conn)
                print("Sending response:", response)
                conn.sendall(str.encode(response))

            except Exception as exception:  # pylint: disable=W0703
                print(f"Exception handling client: {exception}")
                break

        print("Lost connection")
        conn.close()


if __name__ == "__main__":
    server = MultiplayerServer()
    server.run()
