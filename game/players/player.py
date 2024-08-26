from game.visuals.visual_board import VisualBoard, VisualBoardEnemyView
from game.interface.ship import Ship
from game.visuals.visual_ship import Visual_Ship
import json

COMMAND_CREATE_ROOM = "create_room"
COMMAND_JOIN_ROOM_WITH_ID = "join_room_with_id"
COMMAND_JOIN_RANDOM_ROOM = "join_random_room"
COMMAND_SEND_BOARD = "send_board"
COMMAND_EXIT_ROOM = "exit_room"
COMMAND_HAS_OPPONENT_JOINED = "has_opponent_joined"
COMMAND_IS_OPPONENT_READY = "is_opponent_ready"

COMMAND_REGISTER_SHOT = "register_shot"
COMMAND_ASK_TO_RECEIVE_SHOT = "ask_to_receive_shot"
COMMAND_CHANGE_ROOM_PUBLICITY = "change_room_publicity"
COMMAND_REQUEST_ENEMY_BOARD = "request_enemy_board"


class Player:
    def __init__(self, name, network_client):
        self.name = name
        self.network_client = network_client

        self.board = VisualBoard(x=70, y=100)
        self.enemy_board_view = VisualBoardEnemyView(x=700, y=100)

        self.has_sent_board = False
        self.is_turn = False
        self.turn_end_time = None

        self.is_in_finished_battle = False
        self.is_winner = False

    def send_command(self, command_type, **kwargs):
        command_data = {"command": command_type, "args": kwargs}
        command_json = json.dumps(command_data)
        response_json = self.network_client.send(command_json)
        response = json.loads(response_json)
        return response

    def create_room(self):
        response = self.send_command(COMMAND_CREATE_ROOM, client_name=self.name)

        return response

    def join_room_with_id(self, room_id):
        response = self.send_command(
            COMMAND_JOIN_ROOM_WITH_ID, room_id=room_id, client_name=self.name
        )

        return response

    def join_random_room(self):
        response = self.send_command(COMMAND_JOIN_RANDOM_ROOM, client_name=self.name)

        return response

    def send_board(self):
        board_json = self.board.serialize_board()
        response = self.send_command(COMMAND_SEND_BOARD, board_json=board_json)

        self.has_sent_board = response["status"]
        return response

    def request_enemy_board(self):
        response = self.send_command(COMMAND_REQUEST_ENEMY_BOARD)

        if response["status"] != "success":
            return

        board_data = response["args"]["enemy_board_data"]

        self.enemy_board_view.reveal_ships_from_board_data(board_data)

    def exit_room(self):
        response = self.send_command(COMMAND_EXIT_ROOM)

        return response

    def change_room_publicity(self):
        response = self.send_command(COMMAND_CHANGE_ROOM_PUBLICITY)

        return response

    def has_opponent_joined(self):
        response = self.send_command(COMMAND_HAS_OPPONENT_JOINED)

        return response

    def is_opponent_ready(self):
        response = self.send_command(COMMAND_IS_OPPONENT_READY)

        if response["status"] == "success":
            self.is_turn = response["args"]["is_turn"]

        return response

    def shot(self, row, col):
        response = self.send_command(COMMAND_REGISTER_SHOT, row=row, col=col)
        response_args = response["args"]

        if response["status"] == "error":
            if not response_args.get("is_player_turn", False):
                return

            if not response_args.get("is_shot_valid", False):
                return

        self.enemy_board_view.register_shot(row, col, response_args["has_hit_ship"])

        if response_args["has_sunk_ship"]:
            ship = Ship.deserialize(response_args["sunk_ship"])
            self.enemy_board_view.reveal_ship(ship, reveal_adjacent=True)

        self.is_turn = response_args["is_turn"]
        self.turn_end_time = response_args["turn_end_time"]

        self.is_in_finished_battle = response_args["has_battle_ended"]
        self.is_winner = response_args["is_winner"]

        return response

    def ask_to_receive_shot(self):
        response = self.send_command(COMMAND_ASK_TO_RECEIVE_SHOT)

        if response["status"] == "error":
            return

        response_args = response["args"]
        row, col = response_args["row"], response_args["col"]

        self.board.register_shot(row, col)
        self.is_turn = response_args["is_turn"]
        self.turn_end_time = response_args["turn_end_time"]

        self.is_in_finished_battle = response_args["has_battle_ended"]
        self.is_winner = response_args["is_winner"]
