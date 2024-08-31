import pytest
from unittest.mock import MagicMock
from game.server.room import Room, RoomClient
from game.interface.base_board import BaseBoard


# Mocking BaseBoard since it involves more complex logic that's not the focus of these tests
@pytest.fixture
def mock_base_board():
    board = MagicMock(spec=BaseBoard)
    board.is_coordinate_in_board.return_value = True
    board.is_coordinate_shot_at.return_value = False
    board.are_all_ships_sunk.return_value = False
    board.register_shot.return_value = (True, False, "MockShip")
    return board


@pytest.fixture
def mock_client():
    return MagicMock()


def test_room_client_add_board(mock_client, mock_base_board):
    client = RoomClient(mock_client, "TestClient")
    BaseBoard.deserialize_board = MagicMock(return_value=mock_base_board)

    board_json = '{"some": "json"}'
    assert client.add_board(board_json) == True
    assert client.board == mock_base_board
    assert client.has_board == True


def test_room_client_is_shot_valid(mock_client, mock_base_board):
    client = RoomClient(mock_client, "TestClient")
    client.board = mock_base_board

    assert client.is_shot_valid(1, 1) == True
    mock_base_board.is_coordinate_shot_at.return_value = True
    assert client.is_shot_valid(1, 1) == False


def test_room_init(mock_client):
    room = Room("room123", mock_client, "Creator", 60)
    assert room.room_id == "room123"
    assert len(room.clients) == 1
    assert mock_client in room.clients
    assert room.time_per_turn == 60


def test_room_add_player(mock_client):
    room = Room("room123", mock_client, "Creator", 60)
    new_client = MagicMock()

    assert room.add_player(new_client, "NewPlayer") == True
    assert len(room.clients) == 2
    assert room.is_full == True
    assert room.add_player(new_client, "NewPlayer") == False


def test_room_is_client_turn(mock_client):
    room = Room("room123", mock_client, "Creator", 60)
    room.clients[mock_client].is_turn = True
    assert room.is_client_turn(mock_client) == True


def test_room_give_client_turn(mock_client):
    room = Room("room123", mock_client, "Creator", 60)
    new_client = MagicMock()
    room.add_player(new_client, "NewPlayer")

    room.give_client_turn(new_client)
    assert room.is_client_turn(new_client) == True
    assert room.is_client_turn(mock_client) == False


def test_room_start_battle(mock_client):
    room = Room("room123", mock_client, "Creator", 60)
    new_client = MagicMock()
    room.add_player(new_client, "NewPlayer")
    room.start_battle()

    assert room.has_battle_started == True
    assert room.is_client_turn(mock_client) == True or room.is_client_turn(new_client) == True


def test_room_register_shot_for_client(mock_client, mock_base_board):
    room = Room("room123", mock_client, "Creator", 60)
    new_client = MagicMock()
    room.add_player(new_client, "NewPlayer")

    room.clients[mock_client].board = mock_base_board
    room.clients[new_client].board = mock_base_board

    result = room.register_shot_for_client(mock_client, 1, 1)
    assert result == (True, False, "MockShip", False, False, room.turn_end_time)


def test_room_check_has_battle_ended(mock_client, mock_base_board):
    room = Room("room123", mock_client, "Creator", 60)
    room.clients[mock_client].board = mock_base_board

    mock_base_board.are_all_ships_sunk.return_value = True
    assert room.check_has_battle_ended() == True
    assert room.has_battle_ended == True
    assert room.loser == mock_client
