import socket
import random
import json

from _thread import start_new_thread
from game.server.room import Room
from game.server.command_handler import CommandHandler


class Server:
    def __init__(self, server="localhost", port=5555):
        self.server = server
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rooms = {}
        self.clients_to_rooms = {}
        self.command_handler = CommandHandler(self)
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

    def generate_unique_room_id(self):
        while True:
            room_id = str(random.randint(100000, 999999))
            if room_id not in self.rooms:
                return room_id

    def create_room(self, client):
        if self.is_client_in_room(client):
            return self.error_response("Client is already in a room!")

        room_id = self.generate_unique_room_id()
        room = Room(room_id, client)
        self.rooms[room_id] = room
        self.clients_to_rooms[client] = room_id
        print(f"Room {room_id} created")
        return self.success_response(f"Room {room_id} created")

    def join_room_with_id(self, room_id, client):
        if self.is_client_in_room(client):
            return self.error_response("Client is already in a room!")

        if not self.is_room_exists(room_id):
            return self.error_response("Room ID not found.")

        room = self.rooms[room_id]
        if not room.add_player(client):
            return self.error_response("Room is full or player is already in the room.")

        self.clients_to_rooms[client] = room_id
        return self.success_response(f"Joined room {room_id}")

    def join_random_room(self, client):
        if self.is_client_in_room(client):
            return self.error_response("Client is already in a room!")

        for room in self.rooms.values():
            if room.add_player(client):
                self.clients_to_rooms[client] = room.room_id
                return self.success_response(f"Successfully joined room {room.room_id}")

        return self.error_response("No available rooms to join")

    def exit_room(self, client):
        if not self.is_client_in_room(client):
            return self.error_response("Client is not in a room!")

        room_id = self.clients_to_rooms.pop(client)
        self.rooms.pop(room_id)

        return self.success_response(f"Client exited from room {room_id}")

    def has_opponent_joined(self, client):
        if not self.is_client_in_room(client):
            return self.error_response("Client is not in a room!")

        room_id = self.clients_to_rooms.get(client)
        room = self.rooms[room_id]

        if room.is_full:
            return self.success_response("Opponent has joined the room!")

        return self.error_response("Opponent has not joined the room!")

    def receive_board(self, client, board_json):
        if not self.is_client_in_room(client):
            return self.error_response("Client is not in a room!")

        room_id = self.clients_to_rooms.get(client)
        room = self.rooms[room_id]

        if room.add_board_for_client(client, board_json):
            return self.success_response("Board added successfully!")

        return self.error_response("Invalid board!")

    def is_opponent_ready(self, client):
        if not self.is_client_in_room(client):
            return self.error_response("Client is not in a room!")

        room_id = self.clients_to_rooms.get(client)
        room = self.rooms[room_id]

        opponent = room.get_opponent_client(client)

        if opponent == None:
            return self.error_response("No opponent found!")

        if not room.does_client_have_board(opponent):
            return self.error_response("Opponent has no board yet!")

        room.start_battle()

        return self.success_response(
            "Starting game!", is_turn=room.is_client_turn(client)
        )

    def register_shot(self, client, row, col):
        if not self.is_client_in_room(client):
            return self.error_response("Client is not in a room!")

        room_id = self.clients_to_rooms.get(client)
        room = self.rooms[room_id]

        if not room.is_client_turn(client):
            return self.error_response("Not player's turn!", is_player_turn=False)

        if not room.is_client_shot_valid(client, row, col):
            return self.error_response("Invalid shot", is_shot_valid=False)

        is_ship_hit, is_ship_sunk, ship = room.register_shot_for_client(
            client, row, col
        )
        is_turn = room.is_client_turn(client)

        return self.success_response(
            "Shot registered!",
            has_hit_ship=is_ship_hit,
            has_sunk_ship=is_ship_sunk,
            sunk_ship=ship.serialize() if is_ship_sunk else None,
            is_turn=is_turn,
            turn_end_time=0,
        )

    def send_opponents_shot(self, client):
        if not self.is_client_in_room(client):
            return self.error_response("Client is not in a room!")

        room_id = self.clients_to_rooms.get(client)
        room = self.rooms[room_id]

        last_shot = room.give_shot_from_history(client)
        if last_shot == None:
            return self.error_response("Client has not made a shot yet!")

        row, col = last_shot
        is_turn = room.is_client_turn(client)

        return self.success_response(
            "Shot was made by the opponent!",
            row=row,
            col=col,
            is_turn=is_turn,
            turn_end_time=0,
        )

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

    def is_client_in_room(self, client):
        return client in self.clients_to_rooms

    def is_room_exists(self, room_id):
        return room_id in self.rooms

    def format_response(self, status, message, **kwargs):
        response_data = {"status": status, "message": message, "args": kwargs}
        response_json = json.dumps(response_data)
        return response_json

    def success_response(self, message, **kwargs):
        return self.format_response("success", message, **kwargs)

    def error_response(self, message, **kwargs):
        return self.format_response("error", message, **kwargs)


if __name__ == "__main__":
    server = Server()
    server.run()
