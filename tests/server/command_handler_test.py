import json
import pytest

from unittest.mock import MagicMock
from game.server.command_handler import CommandHandler
from game.players import command_literals


@pytest.fixture
def mock_server():
    server = MagicMock()
    server.create_room.return_value = "Room created"
    server.join_room_with_id.return_value = "Joined room with ID"
    server.join_random_room.return_value = "Joined random room"
    server.receive_board.return_value = "Board received"
    server.is_opponent_ready.return_value = "Opponent ready"
    server.exit_room.return_value = "Exited room"
    server.has_opponent_joined.return_value = "Opponent joined"
    server.register_shot.return_value = "Shot registered"
    server.send_opponents_shot.return_value = "Shot sent"
    server.change_room_publicity.return_value = "Room publicity changed"
    server.send_enemy_board.return_value = "Enemy board sent"
    return server


@pytest.fixture
def command_handler(mock_server):
    return CommandHandler(mock_server)


@pytest.fixture
def mock_client():
    return MagicMock()


def test_handle_command_create_room(command_handler, mock_client):
    json_command = json.dumps({"command": command_literals.COMMAND_CREATE_ROOM, "args": {"client_name": "Player1"}})
    response = command_handler.handle_command(json_command, mock_client)
    assert response == "Room created"
    command_handler.server.create_room.assert_called_once_with(mock_client, client_name="Player1")


def test_handle_command_join_room_with_id(command_handler, mock_client):
    json_command = json.dumps(
        {"command": command_literals.COMMAND_JOIN_ROOM_WITH_ID, "args": {"room_id": "1234", "client_name": "Player1"}}
    )
    response = command_handler.handle_command(json_command, mock_client)
    assert response == "Joined room with ID"
    command_handler.server.join_room_with_id.assert_called_once_with(mock_client, room_id="1234", client_name="Player1")


def test_handle_command_missing_command(command_handler, mock_client):
    json_command = json.dumps({"args": {"client_name": "Player1"}})
    response = command_handler.handle_command(json_command, mock_client)
    assert response == CommandHandler.error_response("Missing command")


def test_handle_command_unknown_command(command_handler, mock_client):
    json_command = json.dumps({"command": "UNKNOWN_COMMAND", "args": {"client_name": "Player1"}})
    response = command_handler.handle_command(json_command, mock_client)
    assert response == CommandHandler.error_response("Unknown command")


def test_handle_command_missing_arguments(command_handler, mock_client):
    json_command = json.dumps({"command": command_literals.COMMAND_CREATE_ROOM, "args": {}})
    response = command_handler.handle_command(json_command, mock_client)
    assert response == CommandHandler.error_response("Missing arguments: client_name")


def test_handle_command_invalid_json(command_handler, mock_client):
    json_command = '{"command": "CREATE_ROOM", "args": {"client_name": "Player1"'  # Invalid JSON
    response = command_handler.handle_command(json_command, mock_client)
    assert response == CommandHandler.error_response("Invalid JSON format")


def test_handle_command_server_error(command_handler, mock_client):
    command_handler.server.create_room.side_effect = Exception("Server error")
    json_command = json.dumps({"command": command_literals.COMMAND_CREATE_ROOM, "args": {"client_name": "Player1"}})
    response = command_handler.handle_command(json_command, mock_client)
    assert response == CommandHandler.error_response("Server error!")


def test_format_response():
    response = CommandHandler.format_response("success", "Operation completed", key="value")
    expected_response = json.dumps({"status": "success", "message": "Operation completed", "args": {"key": "value"}})
    assert response == expected_response


def test_success_response():
    response = CommandHandler.success_response("Operation completed", key="value")
    expected_response = json.dumps({"status": "success", "message": "Operation completed", "args": {"key": "value"}})
    assert response == expected_response


def test_error_response():
    response = CommandHandler.error_response("Operation failed", key="value")
    expected_response = json.dumps({"status": "error", "message": "Operation failed", "args": {"key": "value"}})
    assert response == expected_response
