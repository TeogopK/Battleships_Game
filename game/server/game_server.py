import random
import json

from game.server.room import Room
from game.server.command_handler import CommandHandler
from game.players.battle_bot import BattleBot
from game.server.network import OfflineNetwork
from game.players import command_literals


class GameServer:
    def __init__(self, time_per_turn=None):
        self.rooms = {}
        self.clients_to_rooms = {}
        self.command_handler = CommandHandler(self)
        self.time_per_turn = time_per_turn

    def run(self):
        pass

    def generate_unique_room_id(self):
        while True:
            room_id = str(random.randint(100000, 999999))
            if room_id not in self.rooms:
                return room_id

    def create_room(self, client, client_name):
        if self.is_client_in_room(client):
            return CommandHandler.error_response("Client is already in a room!")

        room_id = self.generate_unique_room_id()
        room = Room(room_id, client, client_name, self.time_per_turn)
        self.rooms[room_id] = room
        self.clients_to_rooms[client] = room_id
        return CommandHandler.success_response(f"Room {room_id} created!", room_id=room_id)

    def join_room_with_id(self, client, room_id, client_name):
        if self.is_client_in_room(client):
            return CommandHandler.error_response("Client is already in a room!")

        if not self.does_room_exist(room_id):
            return CommandHandler.error_response("Room ID not found!")

        room = self.rooms[room_id]
        if not room.add_player(client, client_name):
            return CommandHandler.error_response("Room is full or player is already in the room!")

        return self._finish_joining_room(client, room)

    def _finish_joining_room(self, client, room):
        self.clients_to_rooms[client] = room.room_id

        opponent_name = room.get_opponent_room_client(client).client_name
        return CommandHandler.success_response(
            f"Joined room {room.room_id}!",
            room_id=room.room_id,
            opponent_name=opponent_name,
        )

    def join_random_room(self, client, client_name):
        if self.is_client_in_room(client):
            return CommandHandler.error_response("Client is already in a room!")

        for room in self.rooms.values():
            if room.is_private:
                continue
            if room.add_player(client, client_name):
                return self._finish_joining_room(client, room)

        return CommandHandler.error_response("No available rooms to join!")

    def change_room_publicity(self, client):
        if not self.is_client_in_room(client):
            return CommandHandler.error_response("Client is not in a room!")

        room_id = self.clients_to_rooms.get(client)
        room = self.rooms[room_id]

        is_private = room.change_publicity()

        return CommandHandler.success_response(f"Room {room_id} publicity changed!", is_private=is_private)

    def exit_room(self, client):
        if not self.is_client_in_room(client):
            return CommandHandler.error_response("Client is not in a room!")

        room_id = self.clients_to_rooms.pop(client)
        self.rooms.pop(room_id)

        return CommandHandler.success_response(f"Client exited from room {room_id}!")

    def has_opponent_joined(self, client):
        if not self.is_client_in_room(client):
            return CommandHandler.error_response("Client is not in a room!")

        room_id = self.clients_to_rooms.get(client)
        room = self.rooms[room_id]

        if not room.is_full:
            return CommandHandler.error_response("Opponent has not joined the room!")

        opponent_name = room.get_opponent_room_client(client).client_name
        return CommandHandler.success_response(
            f"Opponent {opponent_name} has joined the room!",
            opponent_name=opponent_name,
        )

    def receive_board(self, client, board_json):
        if not self.is_client_in_room(client):
            return CommandHandler.error_response("Client is not in a room!")

        room_id = self.clients_to_rooms.get(client)
        room = self.rooms[room_id]

        if not room.add_board_for_client(client, board_json):
            return CommandHandler.error_response("Invalid board!")

        return CommandHandler.success_response("Board added successfully!")

    def is_opponent_ready(self, client):
        if not self.is_client_in_room(client):
            return CommandHandler.error_response("Client is not in a room!")

        room_id = self.clients_to_rooms.get(client)
        room = self.rooms[room_id]

        opponent = room.get_opponent_room_client(client)

        if opponent is None:
            return CommandHandler.error_response("No opponent found!")

        if not room.does_client_have_board(opponent.client):
            return CommandHandler.error_response("Opponent has no board yet!")

        room.start_battle()

        return CommandHandler.success_response(
            "Starting game!",
            is_turn=room.is_client_turn(client),
            turn_end_time=room.turn_end_time,
        )

    @staticmethod
    def _send_end_battle_response(client, room):
        return CommandHandler.error_response(
            "The battle has ended!",
            has_battle_ended=room.has_battle_ended,
            is_winner=room.is_client_winner(client),
            is_timeout=room.is_timeout,
        )

    def register_shot(self, client, row, col):
        if not self.is_client_in_room(client):
            return CommandHandler.error_response("Client is not in a room!")

        room_id = self.clients_to_rooms.get(client)
        room = self.rooms[room_id]

        if room.has_battle_ended:
            return GameServer._send_end_battle_response(client, room)

        if not room.is_client_turn(client):
            return CommandHandler.error_response("Not player's turn!", is_player_turn=False)

        if room.is_turn_late():
            room.end_battle_due_to_timeout()
            return GameServer._send_end_battle_response(client, room)

        if not room.is_client_shot_valid(client, row, col):
            return CommandHandler.error_response("Invalid shot!", is_shot_valid=False)

        (
            is_ship_hit,
            is_ship_sunk,
            ship,
            has_battle_ended,
            is_winner,
            room.turn_end_time,
        ) = room.register_shot_for_client(client, row, col)
        is_turn = room.is_client_turn(client)

        return CommandHandler.success_response(
            "Shot registered!",
            has_hit_ship=is_ship_hit,
            has_sunk_ship=is_ship_sunk,
            sunk_ship=ship.serialize() if is_ship_sunk else None,
            is_turn=is_turn,
            turn_end_time=room.turn_end_time,
            has_battle_ended=has_battle_ended,
            is_winner=is_winner,
            is_timeout=room.is_timeout,
        )

    def send_opponents_shot(self, client):
        if not self.is_client_in_room(client):
            return CommandHandler.error_response("Client is not in a room!")

        room_id = self.clients_to_rooms.get(client)
        room = self.rooms[room_id]

        if room.is_turn_late():
            room.end_battle_due_to_timeout()
            return GameServer._send_end_battle_response(client, room)

        last_shot = room.give_shot_from_history(client)
        if last_shot is None:
            return CommandHandler.error_response("Client has not made a shot yet!")

        (
            row,
            col,
            is_turn,
            has_battle_ended,
            is_winner,
            turn_end_time,
        ) = last_shot

        return CommandHandler.success_response(
            "Shot was made by the opponent!",
            row=row,
            col=col,
            is_turn=is_turn,
            turn_end_time=turn_end_time,
            has_battle_ended=has_battle_ended,
            is_winner=is_winner,
            is_timeout=room.is_timeout,
        )

    def send_enemy_board(self, client):
        if not self.is_client_in_room(client):
            return CommandHandler.error_response("Client is not in a room!")

        room_id = self.clients_to_rooms.get(client)
        room = self.rooms[room_id]

        if not room.has_battle_ended:
            return CommandHandler.error_response("Battle is still going!")

        enemy_board_data = room.get_enemy_board(client)

        return CommandHandler.success_response("Return the enemy board!", enemy_board_data=enemy_board_data)

    def is_client_in_room(self, client):
        return client in self.clients_to_rooms

    def does_room_exist(self, room_id):
        return room_id in self.rooms


class SinglePlayerServer(GameServer):
    def __init__(self):
        super().__init__()
        self.battle_bot = BattleBot(OfflineNetwork(is_player=False))
        self.battle_bot.network_client.add_server_instance(self)

    def set_up_game_room(self, player):
        player.create_room()
        response = self.battle_bot.join_random_room()
        self.battle_bot.send_board()

        room_id = response["args"]["room_id"]

        return room_id

    def handle_offline_client(self, command, is_player):
        client = self.battle_bot.name if not is_player else "Player"
        response = self.command_handler.handle_command(command, client)

        if is_player:
            command_json = json.loads(command)
            if command_json.get("command") == command_literals.COMMAND_REGISTER_SHOT:
                self.battle_bot.start_main_loop()

        return response
