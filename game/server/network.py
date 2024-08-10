import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.101"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.id = self.connect()
        print(f"Connected with ID: {self.id}")

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.settimeout(5)
            return self.client.recv(2048).decode()
        except socket.timeout:
            raise ConnectionError(
                "Connection timed out while trying to receive initial data.")
        except socket.error as e:
            raise ConnectionError(f"Socket error: {e}")

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            self.client.settimeout(5)
            response = self.client.recv(2048).decode()
            return response
        except socket.timeout:
            print("Socket timed out while waiting for a response.")
        except socket.error as e:
            print(f"Socket error: {e}")
        return None

    def close(self):
        try:
            self.client.close()
        except socket.error as e:
            print(f"Socket error during close: {e}")

    def run(self):
        try:
            while True:
                user_input = input(
                    "> ")
                if user_input.lower() == 'quit':
                    print("Exiting...")
                    break
                response = self.send(user_input)
                if response:
                    print(f"< {response}")
        finally:
            self.close()


if __name__ == "__main__":
    netw = Network()
    netw.run()
