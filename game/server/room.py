from time import time

from game.interface.base_board import BaseBoard


class RoomClient:
    def __init__(self, client, client_name):
        self.client = client
        self.client_name = client_name
        self.board = None
        self.shot_history = []
        self.has_board = False

        self.is_turn = False

    def add_board(self, board_json):
        try:
            self.board = BaseBoard.deserialize_board(board_json)
        except ValueError as e:
            print(e)
            return False

        self.has_board = True
        return True

    def is_shot_valid(self, row, col):
        return self.board.is_coordinate_in_board(
            row, col
        ) and not self.board.is_coordinate_shot_at(row, col)

    def are_all_player_ships_sunk(self):
        return self.board.are_all_ships_sunk()

    def add_shot_history_of_enemy(
        self, row, col, is_turn, has_battle_ended, is_winner, turn_end_time
    ):
        self.shot_history.append(
            (row, col, is_turn, has_battle_ended, is_winner, turn_end_time)
        )


class Room:
    def __init__(self, room_id, client, client_name, time_per_turn):
        self.room_id = room_id
        self.clients = {client: RoomClient(client, client_name)}
        self.max_players = 2
        self.is_private = False
        self.is_full = False

        self.has_battle_started = False
        self.has_battle_ended = False
        self.loser = None

        self.time_per_turn = time_per_turn
        self.turn_end_time = None
        self.is_timeout = False

    def change_publicity(self):
        self.is_private = not self.is_private
        return self.is_private

    def add_board_for_client(self, client, board_json):
        return self.clients[client].add_board(board_json)

    def add_player(self, new_client, client_name):
        if len(self.clients) >= self.max_players:
            return False

        if new_client in self.clients:
            return False

        self.clients[new_client] = RoomClient(new_client, client_name)

        self.is_full = len(self.clients) == self.max_players

        return True

    def is_client_turn(self, client):
        return self.clients[client].is_turn

    def give_client_turn(self, client):
        self.clients[client].is_turn = True
        self.get_opponent_client(client).is_turn = False
        self.turn_end_time = self._get_end_of_turn()

    def take_client_turn(self, client):
        self.clients[client].is_turn = False
        self.get_opponent_client(client).is_turn = True
        self.turn_end_time = self._get_end_of_turn()

    def is_client_shot_valid(self, client, row, col):
        target_client = self.get_opponent_client(client)
        return target_client.is_shot_valid(row, col)

    def register_shot_for_client(self, client, row, col):
        target_client = self.get_opponent_client(client)
        is_ship_hit, is_ship_sunk, ship = target_client.board.register_shot(row, col)

        if is_ship_hit:
            self.give_client_turn(client)
        else:
            self.take_client_turn(client)

        self.check_has_battle_ended()

        target_client.add_shot_history_of_enemy(
            row,
            col,
            target_client.is_turn,
            self.has_battle_ended,
            self.is_client_winner(target_client.client),
            self.turn_end_time,
        )

        return (
            is_ship_hit,
            is_ship_sunk,
            ship,
            self.has_battle_ended,
            self.is_client_winner(client),
            self.turn_end_time,
        )

    def give_shot_from_history(self, client):
        shot_history = self.clients[client].shot_history

        if len(shot_history) == 0:
            return None

        return shot_history.pop(0)

    def get_opponent_client(self, client):
        for opponent_client in self.clients:
            if opponent_client != client:
                return self.clients[opponent_client]
        return None

    def does_client_have_board(self, client):
        return client.has_board

    def start_battle(self):
        if self.has_battle_started:
            return

        self.has_battle_started = True
        for client in self.clients:

            self.give_client_turn(client)
            break

    def is_turn_late(self):
        if self.time_per_turn == None:
            return False

        self.is_timeout = self.turn_end_time - time() < 0
        return self.is_timeout

    def _get_end_of_turn(self):
        if self.time_per_turn == None:
            return time()
        return time() + self.time_per_turn

    def end_battle_due_to_timeout(self):
        self.has_battle_ended = True

        for client in self.clients:
            if self.is_client_turn(client):
                self.loser = client

    def check_has_battle_ended(self):
        for room_client in self.clients.values():
            if room_client.are_all_player_ships_sunk():
                self.has_battle_ended = True
                self.loser = room_client.client
                break

        return self.has_battle_ended

    def is_client_winner(self, client):
        return self.check_has_battle_ended() and self.loser != client

    def get_enemy_board(self, client):
        opponent = self.get_opponent_client(client)
        return opponent.board.serialize_board()
