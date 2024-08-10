class CommandHandler:
    def __init__(self, server):
        self.server = server
        self.command_map = {
            "create-room": self.handle_create_room,
            "join-room-with-id": self.handle_join_room_with_id,
            "join-random-room": self.handle_join_random_room,
            "exit-room": self.handle_exit_room,
        }

    def handle_command(self, command, client):
        parts = command.split()
        if not parts:
            return self.server.error_response("Invalid command")

        cmd = parts[0]
        handler = self.command_map.get(cmd, self.handle_unknown_command)
        return handler(parts, client)

    def handle_create_room(self, parts, client):
        if len(parts) != 1:
            return self.server.error_response("Invalid command format for 'create-room'")
        return self.server.create_room(client)

    def handle_join_room_with_id(self, parts, client):
        if len(parts) != 2:
            return self.server.error_response("Room ID required")
        room_id = parts[1]
        return self.server.join_room_with_id(room_id, client)

    def handle_join_random_room(self, parts, client):
        if len(parts) != 1:
            return self.server.error_response("Invalid command format for 'join-random-room'")
        return self.server.join_random_room(client)

    def handle_exit_room(self, parts, client):
        if len(parts) != 1:
            return self.server.error_response("Invalid command format for 'exit-room'")
        return self.server.exit_room(client)

    def handle_unknown_command(self, parts, client):
        return self.server.error_response("Unknown command")
