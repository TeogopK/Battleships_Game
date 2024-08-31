import pytest
from game.interface.ship import Ship


@pytest.fixture
def horizontal_ship():
    return Ship(ship_length=3, row=2, col=3, is_horizontal=True)


@pytest.fixture
def vertical_ship():
    return Ship(ship_length=3, row=2, col=3, is_horizontal=False)


def test_ship_initialization(horizontal_ship):
    assert horizontal_ship.ship_length == 3
    assert horizontal_ship.is_horizontal is True
    assert horizontal_ship.is_alive is True
    assert horizontal_ship.coordinates == [(2, 3), (2, 4), (2, 5)]
    assert horizontal_ship.sunk_coordinates == set()


def test_flip_orientation(horizontal_ship):
    horizontal_ship.flip()
    assert horizontal_ship.is_horizontal is False
    assert horizontal_ship.coordinates == [(2, 3), (3, 3), (4, 3)]


def test_move_updates_coordinates(horizontal_ship):
    horizontal_ship.move(row=1, col=1, is_horizontal=False)
    assert horizontal_ship.is_horizontal is False
    assert horizontal_ship.coordinates == [(1, 1), (2, 1), (3, 1)]


def test_marking_sunk_coordinates(horizontal_ship):
    horizontal_ship.sunk_coordinate(2, 3)
    assert (2, 3) in horizontal_ship.sunk_coordinates
    assert horizontal_ship.is_alive is True

    horizontal_ship.sunk_coordinate(2, 4)
    assert (2, 4) in horizontal_ship.sunk_coordinates
    assert horizontal_ship.is_alive is True


def test_repair_coordinate(horizontal_ship):
    horizontal_ship.sunk_coordinate(2, 3)
    assert (2, 3) in horizontal_ship.sunk_coordinates

    horizontal_ship.repair_coordinate(2, 3)
    assert (2, 3) not in horizontal_ship.sunk_coordinates


def test_is_sunk(horizontal_ship):
    horizontal_ship.sunk_coordinate(2, 3)
    assert horizontal_ship.is_sunk() is False

    horizontal_ship.sunk_coordinate(2, 4)
    assert horizontal_ship.is_sunk() is False


@pytest.mark.parametrize(
    "row, col, expected",
    [
        (2, 3, True),
        (3, 3, False),
    ],
)
def test_is_coordinate_part_of_ship(horizontal_ship, row, col, expected):
    assert horizontal_ship.is_coordinate_part_of_ship(row, col) == expected


def test_serialize_and_deserialize(horizontal_ship):
    horizontal_ship.sunk_coordinate(2, 3)
    ship_json = horizontal_ship.serialize()
    deserialized_ship = Ship.deserialize(ship_json)

    assert horizontal_ship.ship_length == deserialized_ship.ship_length
    assert horizontal_ship.row == deserialized_ship.row
    assert horizontal_ship.col == deserialized_ship.col
    assert horizontal_ship.is_horizontal == deserialized_ship.is_horizontal
    assert horizontal_ship.is_alive == deserialized_ship.is_alive
    assert horizontal_ship.sunk_coordinates == deserialized_ship.sunk_coordinates
    assert horizontal_ship.coordinates == deserialized_ship.coordinates


def test_ship_representation(horizontal_ship):
    expected_repr = "<Ship with length 3, is horizontal True, at [(2, 3), (2, 4), (2, 5)], with sunk set()>"
    assert repr(horizontal_ship) == expected_repr
