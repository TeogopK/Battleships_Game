"""Module that makes a room environment for a battle between clients."""

from time import time
from game.interface.base_board import BaseBoard


class RoomClient:
    """
    Represents a client in a room, including their game board and shot history.
    """

    def __init__(self, client, client_name):
        """
        Initializes a RoomClient instance.

        Args:
            client (Client): The client associated with this RoomClient.
            client_name (str): The name of the client.
        """
        self.client = client
        self.client_name = client_name
        self.board = None
        self.shot_history = []
        self.has_board = False
        self.is_turn = False

    def add_board(self, board_json):
        """
        Adds a board to the client by deserializing the board JSON.

        Args:
            board_json (str): The JSON representation of the board.

        Returns:
            bool: True if the board was successfully added, False otherwise.
        """
        try:
            self.board = BaseBoard.deserialize_board(board_json)
        except ValueError as exception:
            print(exception)
            return False

        self.has_board = True
        return True

    def is_shot_valid(self, row, col):
        """
        Checks if a shot at the given coordinates is valid.

        Args:
            row (int): The row of the shot.
            col (int): The column of the shot.

        Returns:
            bool: True if the shot is valid, False otherwise.
        """
        return self.board.is_coordinate_in_board(row, col) and not self.board.is_coordinate_shot_at(row, col)

    def are_all_player_ships_sunk(self):
        """
        Checks if all ships on the player's board are sunk.

        Returns:
            bool: True if all ships are sunk, False otherwise.
        """
        return self.board.are_all_ships_sunk()

    def add_shot_history_of_enemy(self, row, col, is_turn, has_battle_ended, is_winner, turn_end_time):
        """
        Adds an entry to the shot history.

        Args:
            row (int): The row of the shot.
            col (int): The column of the shot.
            is_turn (bool): Whether it was the client's turn.
            has_battle_ended (bool): Whether the battle has ended.
            is_winner (bool): Whether the client is a winner.
            turn_end_time (float): The end time of the turn.
        """
        self.shot_history.append((row, col, is_turn, has_battle_ended, is_winner, turn_end_time))


class Room:
    """
    Represents a room where a battle occurs between clients.
    """

    def __init__(self, room_id, client, client_name, time_per_turn):
        """
        Initializes a Room instance.

        Args:
            room_id (str): The unique identifier for the room.
            client (Client): The client creating or joining the room.
            client_name (str): The name of the client.
            time_per_turn (int): The time allowed per turn in seconds.
        """
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
        """
        Toggles the room's privacy setting.

        Returns:
            bool: The new privacy setting (True if private, False otherwise).
        """
        self.is_private = not self.is_private
        return self.is_private

    def add_board_for_client(self, client, board_json):
        """
        Adds a board for a specific client.

        Args:
            client (Client): The client to add the board for.
            board_json (str): The JSON representation of the board.

        Returns:
            bool: True if the board was successfully added, False otherwise.
        """
        return self.clients[client].add_board(board_json)

    def add_player(self, new_client, client_name):
        """
        Adds a new player to the room.

        Args:
            new_client (Client): The new client to add.
            client_name (str): The name of the new client.

        Returns:
            bool: True if the player was successfully added, False otherwise.
        """
        if len(self.clients) >= self.max_players or new_client in self.clients:
            return False

        self.clients[new_client] = RoomClient(new_client, client_name)
        self.is_full = len(self.clients) == self.max_players
        return True

    def is_client_turn(self, client):
        """
        Checks if it's a specific client's turn.

        Args:
            client (Client): The client to check.

        Returns:
            bool: True if it's the client's turn, False otherwise.
        """
        return self.clients[client].is_turn

    def give_client_turn(self, client):
        """
        Gives the turn to a specific client.

        Args:
            client (Client): The client to give the turn to.
        """
        self.clients[client].is_turn = True
        self.get_opponent_room_client(client).is_turn = False
        self.turn_end_time = self._get_end_of_turn()

    def take_client_turn(self, client):
        """
        Ends the current client's turn and gives the turn to the opponent.

        Args:
            client (Client): The client whose turn is ending.
        """
        self.clients[client].is_turn = False
        self.get_opponent_room_client(client).is_turn = True
        self.turn_end_time = self._get_end_of_turn()

    def is_client_shot_valid(self, client, row, col):
        """
        Checks if a shot from a specific client is valid.

        Args:
            client (Client): The client whose shot is being checked.
            row (int): The row of the shot.
            col (int): The column of the shot.

        Returns:
            bool: True if the shot is valid, False otherwise.
        """
        target_client = self.get_opponent_room_client(client)
        return target_client.is_shot_valid(row, col)

    def register_shot_for_client(self, client, row, col):
        """
        Registers a shot from a specific client.

        Args:
            client (Client): The client making the shot.
            row (int): The row of the shot.
            col (int): The column of the shot.

        Returns:
            tuple: Contains information about the shot result, battle status, and turn end time.
        """
        target_client = self.get_opponent_room_client(client)
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
        """
        Retrieves and removes the next shot from the client's shot history.

        Args:
            client (Client): The client whose shot history is being accessed.

        Returns:
            tuple: The next shot from the history or None if history is empty.
        """
        shot_history = self.clients[client].shot_history
        if len(shot_history) == 0:
            return None

        return shot_history.pop(0)

    def get_opponent_room_client(self, client):
        """
        Gets the RoomClient for the opponent of a specific client.

        Args:
            client (Client): The client whose opponent is being retrieved.

        Returns:
            RoomClient: The opponent's RoomClient or None if no opponent is found.
        """
        for opponent_client, opponent_room_client in self.clients.items():
            if opponent_client != client:
                return opponent_room_client
        return None

    def does_client_have_board(self, client):
        """
        Checks if a specific client has a board.

        Args:
            client (Client): The client to check.

        Returns:
            bool: True if the client has a board, False otherwise.
        """
        return self.clients[client].has_board

    def start_battle(self):
        """
        Starts the battle and assigns turns to the clients.
        """
        if self.has_battle_started:
            return

        self.has_battle_started = True
        for client in self.clients:
            self.give_client_turn(client)
            break

    def is_turn_late(self):
        """
        Checks if the turn time has elapsed.

        Returns:
            bool: True if the turn is late, False otherwise.
        """
        if self.time_per_turn is None:
            return False

        self.is_timeout = self.turn_end_time - time() < 0
        return self.is_timeout

    def _get_end_of_turn(self):
        """
        Calculates the end time of the current turn.

        Returns:
            float: The end time of the turn.
        """
        if self.time_per_turn is None:
            return time()
        return time() + self.time_per_turn

    def end_battle_due_to_timeout(self):
        """
        Ends the battle if a timeout occurs.
        """
        self.has_battle_ended = True
        for client in self.clients:
            if self.is_client_turn(client):
                self.loser = client

    def check_has_battle_ended(self):
        """
        Checks if the battle has ended due to all ships being sunk.

        Returns:
            bool: True if the battle has ended, False otherwise.
        """
        for room_client in self.clients.values():
            if room_client.are_all_player_ships_sunk():
                self.has_battle_ended = True
                self.loser = room_client.client
                break

        return self.has_battle_ended

    def is_client_winner(self, client):
        """
        Checks if a specific client is the winner of the battle.

        Args:
            client (Client): The client to check.

        Returns:
            bool: True if the client is a winner, False otherwise.
        """
        return self.check_has_battle_ended() and self.loser != client

    def get_enemy_board(self, client):
        """
        Gets the serialized board of the opponent for a specific client.

        Args:
            client (Client): The client whose opponent's board is being retrieved.

        Returns:
            str: The JSON representation of the opponent's board.
        """
        opponent = self.get_opponent_room_client(client)
        return opponent.board.serialize_board()
