from game.visuals.visual_board import VisualBoard
import json

COMMAND_CREATE_ROOM = "create-room"
COMMAND_JOIN_ROOM_WITH_ID = "join-room-with-id"
COMMAND_JOIN_RANDOM_ROOM = "join-random-room"
COMMAND_SEND_BOARD = "send-board"
COMMAND_EXIT_ROOM = "exit-room"
COMMAND_HAS_OPPONENT_JOINED = "has-opponent-joined"
COMMAND_CAN_GAME_START = "exit-room"


class Player:
    def __init__(self, name, network_client, x=70, y=100):
        self.name = name
        self.network_client = network_client

        self.board = VisualBoard(x, y)
        self.has_sent_board = False

    def send_command(self, command_type, **kwargs):
        command_data = {"command": command_type, "args": kwargs}
        command_json = json.dumps(command_data)
        response_json = self.network_client.send(command_json)
        response = json.loads(response_json)
        return response

    def create_room(self):
        response = self.send_command(COMMAND_CREATE_ROOM)

        return response

    def join_room_with_id(self, room_id):
        response = self.send_command(COMMAND_JOIN_ROOM_WITH_ID, room_id=room_id)

        return response

    def join_random_room(self):
        response = self.send_command(COMMAND_JOIN_RANDOM_ROOM)

        return response

    def send_board(self):
        board_json = self.board.serialize_board()
        response = self.send_command(COMMAND_SEND_BOARD, board_json=board_json)

        return response

    def exit_room(self):
        response = self.send_command(COMMAND_EXIT_ROOM)

        return response

    def has_opponent_joined(self):
        response = self.send_command(COMMAND_HAS_OPPONENT_JOINED)

        return response

    def ask_can_game_start(self):
        response = self.send_command(COMMAND_SEND_BOARD)

        return response

    def are_all_ships_sunk(self):
        return self.board.are_all_ships_sunk()
