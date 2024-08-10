class Room:
    def __init__(self, room_id, client_id):
        self.room_id = room_id
        self.players = [client_id]
        self.max_players = 2
        self.is_full = False

    def add_player(self, new_client_id):
        if len(self.players) >= self.max_players:
            return False

        if new_client_id in self.players:
            return False

        self.players.append(new_client_id)

        self.is_full = len(self.players) == self.max_players

        return True

    def start_battle(self):
        print(
            f"Battle started in Room {self.room_id} between {self.players[0]} and {self.players[1]}")
