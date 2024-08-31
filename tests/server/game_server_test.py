import json
import pytest
from game.server.game_server import GameServer


@pytest.fixture
def game_server():
    return GameServer()


def test_generate_unique_room_id(game_server):
    room_id1 = game_server.generate_unique_room_id()
    room_id2 = game_server.generate_unique_room_id()
    assert room_id1 != room_id2
    assert len(room_id1) == 6
    assert len(room_id2) == 6


def test_create_room_success(game_server):
    client = "client_1"
    client_name = "Alice"
    response = game_server.create_room(client, client_name)
    assert "success" in response
    assert "Room" in response


def test_create_room_client_already_in_room(game_server):
    client = "client_1"
    client_name = "Alice"
    game_server.create_room(client, client_name)
    response = game_server.create_room(client, client_name)
    assert "error" in response
    assert "Client is already in a room" in response


def test_join_room_with_id_success(game_server):
    client1 = "client_1"
    client2 = "client_2"
    client_name1 = "Alice"
    client_name2 = "Bob"

    response1 = json.loads(game_server.create_room(client1, client_name1))
    room_id = response1["args"]["room_id"]

    response2 = json.loads(game_server.join_room_with_id(client2, room_id, client_name2))
    assert "success" in response2["status"]
    assert room_id in response2["args"]["room_id"]


def test_join_room_with_id_client_already_in_room(game_server):
    client1 = "client_1"
    client_name1 = "Alice"
    client2 = "client_2"

    game_server.create_room(client1, client_name1)
    response = game_server.join_room_with_id(client1, "123456", client_name1)
    assert "error" in response
    assert "Client is already in a room" in response


def test_exit_room_success(game_server):
    client = "client_1"
    client_name = "Alice"
    game_server.create_room(client, client_name)
    response = game_server.exit_room(client)
    assert "success" in response
    assert "Client exited from room" in response


def test_exit_room_client_not_in_room(game_server):
    client = "client_1"
    response = game_server.exit_room(client)
    assert "error" in response
    assert "Client is not in a room" in response
