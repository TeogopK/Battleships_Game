from game.interface.base_board import BaseBoard


class RoomClient:
    def __init__(self, client):
        self.client = client
        self.board = None
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


class Room:
    def __init__(self, room_id, client):
        self.room_id = room_id
        self.clients = {client: RoomClient(client)}
        self.max_players = 2
        self.is_full = False

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

    def start_battle(self):
        print(f"Battle started in Room {self.room_id} between {self.clients[0]} and {self.clients[1]}")
