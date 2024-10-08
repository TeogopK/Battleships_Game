"""Module that handles commands received from clients and executes appropriate server methods."""

import json
from collections import namedtuple
from game.players import command_literals

# Define a Command namedtuple to store command details
Command = namedtuple("Command", ["name", "handler", "required_args"])


class CommandHandler:
    """
    Handles commands received from clients and executes appropriate server methods.
    """

    def __init__(self, server):
        """
        Initializes the CommandHandler with server instance and sets up commands.

        Args:
            server (Server): The server instance that will handle the commands.
        """
        self.server = server
        self.commands = {
            command_literals.COMMAND_CREATE_ROOM: Command(
                command_literals.COMMAND_CREATE_ROOM,
                self.server.create_room,
                ["client_name"],
            ),
            command_literals.COMMAND_JOIN_ROOM_WITH_ID: Command(
                command_literals.COMMAND_JOIN_ROOM_WITH_ID,
                self.server.join_room_with_id,
                ["room_id", "client_name"],
            ),
            command_literals.COMMAND_JOIN_RANDOM_ROOM: Command(
                command_literals.COMMAND_JOIN_RANDOM_ROOM,
                self.server.join_random_room,
                ["client_name"],
            ),
            command_literals.COMMAND_SEND_BOARD: Command(
                command_literals.COMMAND_SEND_BOARD,
                self.server.receive_board,
                ["board_json"],
            ),
            command_literals.COMMAND_IS_OPPONENT_READY: Command(
                command_literals.COMMAND_IS_OPPONENT_READY,
                self.server.is_opponent_ready,
                [],
            ),
            command_literals.COMMAND_EXIT_ROOM: Command(
                command_literals.COMMAND_EXIT_ROOM,
                self.server.exit_room,
                [],
            ),
            command_literals.COMMAND_HAS_OPPONENT_JOINED: Command(
                command_literals.COMMAND_HAS_OPPONENT_JOINED,
                self.server.has_opponent_joined,
                [],
            ),
            command_literals.COMMAND_REGISTER_SHOT: Command(
                command_literals.COMMAND_REGISTER_SHOT,
                self.server.register_shot,
                ["row", "col"],
            ),
            command_literals.COMMAND_ASK_TO_RECEIVE_SHOT: Command(
                command_literals.COMMAND_ASK_TO_RECEIVE_SHOT,
                self.server.send_opponents_shot,
                [],
            ),
            command_literals.COMMAND_CHANGE_ROOM_PUBLICITY: Command(
                command_literals.COMMAND_CHANGE_ROOM_PUBLICITY,
                self.server.change_room_publicity,
                [],
            ),
            command_literals.COMMAND_REQUEST_ENEMY_BOARD: Command(
                command_literals.COMMAND_REQUEST_ENEMY_BOARD,
                self.server.send_enemy_board,
                [],
            ),
        }

    def handle_command(self, json_command, client):
        """
        Handles the incoming command by parsing the JSON and invoking the corresponding server method.

        Args:
            json_command (str): The JSON string representing the command.
            client (Client): The client instance sending the command.

        Returns:
            str: The JSON string representing the response.
        """
        try:
            print(f"Received command: {json_command}")
            command_data = json.loads(json_command)
            cmd = command_data.get("command")
            args = command_data.get("args", {})

            if cmd is None:
                return CommandHandler.error_response("Missing command")

            command = self.commands.get(cmd)
            if command is None:
                return CommandHandler.error_response("Unknown command")

            missing_args = [arg for arg in command.required_args if arg not in args]
            if missing_args:
                return CommandHandler.error_response(f"Missing arguments: {', '.join(missing_args)}")

            return command.handler(client, **args)
        except json.JSONDecodeError:
            return CommandHandler.error_response("Invalid JSON format")
        except Exception as exception:  # pylint: disable=W0703
            print(exception)
            return CommandHandler.error_response("Server error!")

    @staticmethod
    def format_response(status, message, **kwargs):
        """
        Formats the response as a JSON string.

        Args:
            status (str): The status of the response ("success" or "error").
            message (str): The message to include in the response.
            **kwargs: Additional arguments to include in the response.

        Returns:
            str: The JSON string representing the formatted response.
        """
        response_data = {"status": status, "message": message, "args": kwargs}
        response_json = json.dumps(response_data)
        return response_json

    @staticmethod
    def success_response(message, **kwargs):
        """
        Creates a success response.

        Args:
            message (str): The success message.
            **kwargs: Additional arguments to include in the response.

        Returns:
            str: The JSON string representing the success response.
        """
        return CommandHandler.format_response("success", message, **kwargs)

    @staticmethod
    def error_response(message, **kwargs):
        """
        Creates an error response.

        Args:
            message (str): The error message.
            **kwargs: Additional arguments to include in the response.

        Returns:
            str: The JSON string representing the error response.
        """
        return CommandHandler.format_response("error", message, **kwargs)
