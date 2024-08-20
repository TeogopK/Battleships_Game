from game.interface.base_board import BaseBoard


class RoomClient:
    def __init__(self, client):
        self.client = client
        self.board = None
        self.shot_history = []
        self.has_board = False

        self.is_turn = False

    def add_board(self, board_json):
        try:
            self.board = BaseBoard.deserialize_board(board_json)
        except Exception as e:
            print(e)
            return False

        self.has_board = True
        return True

    def is_shot_valid(self, row, col):
        return self.board.is_coordinate_in_board(
            row, col
        ) and not self.board.is_coordinate_shot_at(row, col)


class Room:
    def __init__(self, room_id, client):
        self.room_id = room_id
        self.clients = {client: RoomClient(client)}
        self.max_players = 2
        self.is_full = False
        self.has_battle_started = False

    def add_board_for_client(self, client, board_json):
        return self.clients[client].add_board(board_json)

    def add_player(self, new_client):
        if len(self.clients) >= self.max_players:
            return False

        if new_client in self.clients:
            return False

        self.clients[new_client] = RoomClient(new_client)

        self.is_full = len(self.clients) == self.max_players

        return True

    def is_client_turn(self, client):
        return self.clients[client].is_turn

    def give_client_turn(self, client):
        self.clients[client].is_turn = True
        self.get_opponent_client(client).is_turn = False

    def take_client_turn(self, client):
        self.clients[client].is_turn = False
        self.get_opponent_client(client).is_turn = True

    def convert_coordinates(self, row_string, col_string):
        try:
            row = int(row_string)
            col = int(col_string)
            return row, col
        except ValueError:
            return None, None

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

        target_client.shot_history.append((row, col, target_client.is_turn))

        return is_ship_hit, is_ship_sunk, ship

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

        for client in self.clients.values():
            client.is_turn = True
            self.has_battle_started = True
            break
