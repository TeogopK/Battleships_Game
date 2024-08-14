import json

COMMAND_CREATE_ROOM = "create-room"
COMMAND_JOIN_ROOM_WITH_ID = "join-room-with-id"
COMMAND_JOIN_RANDOM_ROOM = "join-random-room"
COMMAND_SEND_BOARD = "send-board"
COMMAND_EXIT_ROOM = "exit-room"
COMMAND_HAS_OPPONENT_JOINED = "has-opponent-joined"


class Command:
    def __init__(self, name, handler, required_args):
        self.name = name
        self.handler = handler
        self.required_args = required_args


class CommandHandler:
    def __init__(self, server):
        self.server = server
        self.commands = {
            COMMAND_CREATE_ROOM: Command(COMMAND_CREATE_ROOM, self.server.create_room, []),
            COMMAND_JOIN_ROOM_WITH_ID: Command(COMMAND_JOIN_ROOM_WITH_ID, self.server.join_room_with_id, ["room_id"]),
            COMMAND_JOIN_RANDOM_ROOM: Command(COMMAND_JOIN_RANDOM_ROOM, self.server.join_random_room, []),
            COMMAND_SEND_BOARD: Command(COMMAND_SEND_BOARD, self.server.receive_board, ["board_json"]),
            COMMAND_EXIT_ROOM: Command(COMMAND_EXIT_ROOM, self.server.exit_room, []),
            COMMAND_HAS_OPPONENT_JOINED: Command(COMMAND_HAS_OPPONENT_JOINED, self.server.has_opponent_joined, []),
        }

    def handle_command(self, json_command, client):
        try:
            print(f"Received command: {json_command}")
            command_data = json.loads(json_command)
            cmd = command_data.get("command")
            args = command_data.get("args", {})

            if cmd is None:
                return self.server.error_response("Missing command")

            command = self.commands.get(cmd)
            if command is None:
                return self.server.error_response("Unknown command")

            missing_args = [arg for arg in command.required_args if arg not in args]
            if missing_args:
                return self.server.error_response(f"Missing arguments: {', '.join(missing_args)}")

            return command.handler(client, **args)
        except json.JSONDecodeError:
            return self.server.error_response("Invalid JSON format")
