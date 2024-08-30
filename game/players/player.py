"""
Module for managing the Player in the game, including communication with the server
and handling the game state related to the player's actions and board.
"""

import json
from game.visuals.visual_board import VisualBoard, VisualBoardEnemyView
from game.interface.ship import Ship
from game.players import command_literals


class Player:
    """Class representing a player in the game."""

    def __init__(self, name, network_client):
        """
        Initializes a Player object.

        Args:
            name (str): The name of the player.
            network_client (NetworkClient): The network client used for communication.
        """
        self.name = name
        self.network_client = network_client

        self.board = VisualBoard(x=70, y=100)
        self.enemy_board_view = VisualBoardEnemyView(x=700, y=100)

        self.has_sent_board = False
        self.is_turn = False
        self.turn_end_time = None

        self.is_in_finished_battle = False
        self.is_winner = False
        self.is_timeout = False

    def send_command(self, command_type, **kwargs):
        """
        Sends a command to the server and returns the response.

        Args:
            command_type (str): The type of the command to send.
            **kwargs: Additional arguments for the command.

        Returns:
            dict: The server's response as a dictionary.
        """
        command_data = {"command": command_type, "args": kwargs}
        command_json = json.dumps(command_data)
        response_json = self.network_client.send(command_json)
        response = json.loads(response_json)
        return response

    def create_room(self):
        """
        Sends a command to create a new room.

        Returns:
            dict: The server's response indicating the result of the room creation.
        """
        response = self.send_command(command_literals.COMMAND_CREATE_ROOM, client_name=self.name)
        return response

    def join_room_with_id(self, room_id):
        """
        Sends a command to join a room with a specific ID.

        Args:
            room_id (str): The ID of the room to join.

        Returns:
            dict: The server's response indicating the result of joining the room.
        """
        response = self.send_command(
            command_literals.COMMAND_JOIN_ROOM_WITH_ID,
            room_id=room_id,
            client_name=self.name,
        )
        return response

    def join_random_room(self):
        """
        Sends a command to join a random room.

        Returns:
            dict: The server's response indicating the result of joining the random room.
        """
        response = self.send_command(command_literals.COMMAND_JOIN_RANDOM_ROOM, client_name=self.name)
        return response

    def send_board(self):
        """
        Sends the player's board to the server.

        Returns:
            dict: The server's response indicating the result of sending the board.
        """
        board_json = self.board.serialize_board()
        response = self.send_command(command_literals.COMMAND_SEND_BOARD, board_json=board_json)
        self.has_sent_board = response["status"]
        return response

    def request_enemy_board(self):
        """
        Requests the enemy's board data from the server and updates the enemy board view.

        Returns:
            dict: The server's response with the enemy board data.
        """
        response = self.send_command(command_literals.COMMAND_REQUEST_ENEMY_BOARD)

        if response["status"] != "success":
            return

        board_data = response["args"]["enemy_board_data"]
        self.enemy_board_view.reveal_ships_from_board_data(board_data)

    def exit_room(self):
        """
        Sends a command to exit the current room.

        Returns:
            dict: The server's response indicating the result of exiting the room.
        """
        response = self.send_command(command_literals.COMMAND_EXIT_ROOM)
        return response

    def change_room_publicity(self):
        """
        Sends a command to change the publicity of the current room.

        Returns:
            dict: The server's response indicating the result of changing the room's publicity.
        """
        response = self.send_command(command_literals.COMMAND_CHANGE_ROOM_PUBLICITY)
        return response

    def has_opponent_joined(self):
        """
        Sends a command to check if the opponent has joined the room.

        Returns:
            dict: The server's response indicating whether the opponent has joined.
        """
        response = self.send_command(command_literals.COMMAND_HAS_OPPONENT_JOINED)
        return response

    def is_opponent_ready(self):
        """
        Sends a command to check if the opponent is ready.

        Returns:
            dict: The server's response indicating whether the opponent is ready.
        """
        response = self.send_command(command_literals.COMMAND_IS_OPPONENT_READY)

        if response["status"] == "success":
            self.is_turn = response["args"]["is_turn"]
            self.turn_end_time = response["args"]["turn_end_time"]

        return response

    def shot(self, row, col):
        """
        Sends a command to register a shot on the enemy's board.

        Args:
            row (int): The row where the shot is taken.
            col (int): The column where the shot is taken.

        Returns:
            dict: The server's response with the result of the shot.
        """
        response = self.send_command(command_literals.COMMAND_REGISTER_SHOT, row=row, col=col)
        response_args = response["args"]

        if response["status"] == "error":
            if response_args.get("is_timeout", False):
                self._parse_battle_end(response_args)
                return response

            if not response_args.get("is_player_turn", False):
                return response

            if not response_args.get("is_shot_valid", False):
                return response

        self.enemy_board_view.register_shot_on_view(row, col, response_args["has_hit_ship"])

        if response_args["has_sunk_ship"]:
            ship = Ship.deserialize(response_args["sunk_ship"])
            self.enemy_board_view.reveal_ship(ship, reveal_adjacent=True)

        self.is_turn = response_args["is_turn"]
        self.turn_end_time = response_args["turn_end_time"]

        self._parse_battle_end(response_args)
        return response

    def ask_to_receive_shot(self):
        """
        Sends a command to ask for a shot from the opponent.

        Returns:
            dict: The server's response with the shot details and game state.
        """
        response = self.send_command(command_literals.COMMAND_ASK_TO_RECEIVE_SHOT)
        response_args = response.get("args", None)

        if response["status"] == "error":
            if response_args.get("is_timeout", False):
                self._parse_battle_end(response_args)
            return response

        row, col = response_args["row"], response_args["col"]
        self.board.register_shot(row, col)
        self.is_turn = response_args["is_turn"]
        self.turn_end_time = response_args["turn_end_time"]

        self._parse_battle_end(response_args)
        return response

    def _parse_battle_end(self, response_args):
        """
        Parses the battle end state based on the response arguments.

        Args:
            response_args (dict): The arguments from the server response indicating battle end details.
        """
        self.is_in_finished_battle = response_args["has_battle_ended"]
        self.is_winner = response_args["is_winner"]
        self.is_timeout = response_args.get("is_timeout", False)
