import json

COMMAND_CREATE_ROOM = "create_room"
COMMAND_JOIN_ROOM_WITH_ID = "join_room_with_id"
COMMAND_JOIN_RANDOM_ROOM = "join_random_room"
COMMAND_SEND_BOARD = "send_board"
COMMAND_EXIT_ROOM = "exit_room"
COMMAND_HAS_OPPONENT_JOINED = "has_opponent_joined"
COMMAND_REGISTER_SHOT = "register_shot"
COMMAND_ASK_TO_RECEIVE_SHOT = "ask_to_receive_shot"
COMMAND_IS_OPPONENT_READY = "is_opponent_ready"
COMMAND_CHANGE_ROOM_PUBLICITY = "change_room_publicity"
COMMAND_REQUEST_ENEMY_BOARD = "request_enemy_board"


class Command:
    def __init__(self, name, handler, required_args):
        self.name = name
        self.handler = handler
        self.required_args = required_args


class CommandHandler:
    def __init__(self, server):
        self.server = server
        self.commands = {
            COMMAND_CREATE_ROOM: Command(
                COMMAND_CREATE_ROOM, self.server.create_room, ["client_name"]
            ),
            COMMAND_JOIN_ROOM_WITH_ID: Command(
                COMMAND_JOIN_ROOM_WITH_ID,
                self.server.join_room_with_id,
                ["room_id", "client_name"],
            ),
            COMMAND_JOIN_RANDOM_ROOM: Command(
                COMMAND_JOIN_RANDOM_ROOM, self.server.join_random_room, ["client_name"]
            ),
            COMMAND_SEND_BOARD: Command(
                COMMAND_SEND_BOARD, self.server.receive_board, ["board_json"]
            ),
            COMMAND_IS_OPPONENT_READY: Command(
                COMMAND_IS_OPPONENT_READY, self.server.is_opponent_ready, []
            ),
            COMMAND_EXIT_ROOM: Command(COMMAND_EXIT_ROOM, self.server.exit_room, []),
            COMMAND_HAS_OPPONENT_JOINED: Command(
                COMMAND_HAS_OPPONENT_JOINED, self.server.has_opponent_joined, []
            ),
            COMMAND_REGISTER_SHOT: Command(
                COMMAND_REGISTER_SHOT, self.server.register_shot, ["row", "col"]
            ),
            COMMAND_ASK_TO_RECEIVE_SHOT: Command(
                COMMAND_ASK_TO_RECEIVE_SHOT, self.server.send_opponents_shot, []
            ),
            COMMAND_CHANGE_ROOM_PUBLICITY: Command(
                COMMAND_CHANGE_ROOM_PUBLICITY, self.server.change_room_publicity, []
            ),
            COMMAND_REQUEST_ENEMY_BOARD: Command(
                COMMAND_REQUEST_ENEMY_BOARD, self.server.send_enemy_board, []
            ),
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
                return self.server.error_response(
                    f"Missing arguments: {', '.join(missing_args)}"
                )

            return command.handler(client, **args)
        except json.JSONDecodeError:
            return self.server.error_response("Invalid JSON format")
        except Exception as e:
            print(e)
            return self.server.error_response("Server error!")
