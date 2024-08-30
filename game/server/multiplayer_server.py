from game.server.game_server import GameServer
from _thread import start_new_thread
import socket


class MultiplayerServer(GameServer):
    TIME_PER_TURN = 60

    def __init__(self, server="localhost", port=5555):
        super().__init__(self.TIME_PER_TURN)
        self.server = server
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setup_server()

    def setup_server(self):
        try:
            self.s.bind((self.server, self.port))
            self.s.listen(5)
            print(f"Server started, listening on {self.server}:{self.port}")
        except socket.error as e:
            print(f"Socket error during setup: {e}")
            self.s.close()
            raise

    def run(self):
        while True:
            try:
                conn, addr = self.s.accept()
                print(f"Connected to: {addr}")
                start_new_thread(self._handle_client, (conn,))
            except Exception as e:
                print(f"Exception in accepting connections: {e}")

    def _handle_client(self, conn):
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

            except Exception as e:
                print(f"Exception handling client: {e}")
                break

        print("Lost connection")
        conn.close()


if __name__ == "__main__":
    server = MultiplayerServer()
    server.run()
