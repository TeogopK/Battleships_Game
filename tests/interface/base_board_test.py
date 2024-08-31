import json
from game.interface.ship import Ship
from game.interface.base_board import BaseBoard, BaseBoardEnemyView


def test_baseboard_default_initialization():
    board = BaseBoard()
    assert board.rows_count == 10
    assert board.columns_count == 10
    assert len(board.unplaced_ships) == 10
    assert len(board.ships_map) == 0
    assert len(board.taken_coordinates) == 0
    assert len(board.shot_coordinates) == 0
    assert len(board.all_hit_coordinates) == 0


def test_baseboard_custom_initialization():
    custom_ships = {Ship(3), Ship(4)}
    board = BaseBoard(rows_count=5, columns_count=5, unplaced_ships=custom_ships)
    assert board.rows_count == 5
    assert board.columns_count == 5
    assert len(board.unplaced_ships) == 2
    assert len(board.ships_map) == 0
    assert len(board.taken_coordinates) == 0
    assert len(board.shot_coordinates) == 0
    assert len(board.all_hit_coordinates) == 0


def test_is_ship_placement_valid():
    ship = Ship(3)
    board = BaseBoard()

    # Move ship to a valid position
    ship.move(0, 0, True)
    assert board.is_ship_placement_valid(ship) == True

    # Place the ship and then try placing another overlapping ship
    board.place_ship(ship)
    overlapping_ship = Ship(3)
    overlapping_ship.move(0, 0, True)
    assert board.is_ship_placement_valid(overlapping_ship) == False


def test_random_shuffle_ships():
    board = BaseBoard()
    board.random_shuffle_ships()

    # Ensure that the number of ships placed equals the number of ships available initially
    assert len(board.ships_map) > 0
    assert len(board.unplaced_ships) == 0


def test_register_shot():
    board = BaseBoard()
    ship = Ship(2)
    ship.move(0, 0, True)
    board.place_ship(ship)

    # Shoot at an empty spot
    is_hit, is_sunk, _ = board.register_shot(1, 1)
    assert is_hit == False
    assert is_sunk == False

    # Shoot at the ship
    is_hit, is_sunk, hit_ship = board.register_shot(0, 0)
    assert is_hit == True
    assert is_sunk == False
    assert hit_ship == ship


def test_remove_ship():
    board = BaseBoard()
    ship = Ship(2)
    ship.move(0, 0, True)
    board.place_ship(ship)
    assert len(board.ships_map) == 1

    board.remove_ship(ship)
    assert len(board.ships_map[(0, 0)]) == 0
    assert ship in board.unplaced_ships


def test_move_ship():
    board = BaseBoard()
    ship = Ship(2)
    ship.move(0, 0, True)

    board.place_ship(ship)
    board.move_ship(ship, 1, 1, True)

    assert len(board.ships_map[(1, 1)]) == 1
    assert len(board.ships_map[(0, 0)]) == 0
    assert board.get_ship_on_coord(1, 1) == ship


def test_flip_ship():
    board = BaseBoard()
    ship = Ship(2)
    ship.move(0, 0, True)
    board.place_ship(ship)
    assert board.get_ship_on_coord(0, 1) == ship
    assert board.get_ship_on_coord(1, 0) is None

    board.flip_ship(ship)
    assert ship.is_horizontal == False
    assert board.get_ship_on_coord(0, 1) is None
    assert board.get_ship_on_coord(1, 0) == ship


def test_is_coordinate_in_board():
    board = BaseBoard()
    assert board.is_coordinate_in_board(0, 0) == True
    assert board.is_coordinate_in_board(9, 9) == True
    assert board.is_coordinate_in_board(-1, 0) == False
    assert board.is_coordinate_in_board(0, 10) == False


def test_is_coordinate_shot_at():
    board = BaseBoard()
    assert board.is_coordinate_shot_at(0, 0) == False
    board.register_shot(0, 0)
    assert board.is_coordinate_shot_at(0, 0) == True


def test_serialize_board():
    board = BaseBoard()
    ship = Ship(2)
    ship.move(0, 0, True)
    board.place_ship(ship)
    serialized_board = board.serialize_board()
    expected_data = {"rows_count": 10, "columns_count": 10, "ships": [ship.serialize()]}
    assert json.loads(serialized_board) == expected_data


def test_place_ships_from_json():
    board = BaseBoard()
    ship = Ship(2)
    ship.move(0, 0, True)
    board.place_ship(ship)
    board_json = board.serialize_board()
    new_board = BaseBoard.deserialize_board(board_json)
    assert len(new_board.ships_map) == 1
    assert new_board.get_ship_on_coord(0, 0) is not None


def test_are_all_ships_sunk():
    board = BaseBoard()
    ship = Ship(2)
    ship.move(0, 0, True)
    board.place_ship(ship)
    board.register_shot(0, 0)
    board.register_shot(0, 1)
    assert board.are_all_ships_sunk() == True


def test_baseboard_enemy_view_initialization():
    enemy_view = BaseBoardEnemyView()
    assert enemy_view.rows_count == 10
    assert enemy_view.columns_count == 10


def test_register_shot_on_view():
    enemy_view = BaseBoardEnemyView()
    enemy_view.register_shot_on_view(0, 0, True)
    assert enemy_view.shot_coordinates[(0, 0)] == 1
    assert (0, 0) in enemy_view.all_hit_coordinates


def test_reveal_ship():
    enemy_view = BaseBoardEnemyView()
    ship = Ship(2)
    ship.move(0, 0, True)
    result = enemy_view.reveal_ship(ship)
    assert result == True
    assert enemy_view.get_ship_on_coord(0, 0) is not None


def test_reveal_ships_from_board_data():
    board = BaseBoard()
    ship = Ship(2)
    ship.move(0, 0, True)
    board.place_ship(ship)
    board_data = board.serialize_board()
    enemy_view = BaseBoardEnemyView()
    enemy_view.reveal_ships_from_board_data(board_data)
    assert enemy_view.get_ship_on_coord(0, 0) is not None
