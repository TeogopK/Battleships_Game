import pytest
from unittest.mock import patch

from game.visuals.visual_ship import VisualShip
from game.visuals.visual_board import VisualBoard, VisualTile, VisualBoardEnemyView


@pytest.fixture
def visual_board():
    board = VisualBoard(x=0, y=0)
    board.rows_count = 5
    board.columns_count = 5
    board.tiles = [
        [VisualTile(x * VisualTile.TILE_SIZE, y * VisualTile.TILE_SIZE) for x in range(board.columns_count)]
        for y in range(board.rows_count)
    ]
    return board


@pytest.fixture
def visual_board_enemy_view():
    board = VisualBoardEnemyView(x=0, y=0)
    board.rows_count = 5
    board.columns_count = 5
    board.tiles = [
        [VisualTile(x * VisualTile.TILE_SIZE, y * VisualTile.TILE_SIZE) for x in range(board.columns_count)]
        for y in range(board.rows_count)
    ]
    return board


def test_get_tile_screen_placement(visual_board):
    assert visual_board.get_tile_screen_placement(1, 1) == (50, 50)
    assert visual_board.get_tile_screen_placement(0, 0) == (0, 0)


def test_get_right_border(visual_board):
    visual_board.get_tile_size = lambda: 50
    assert visual_board.get_right_border() == 250


def test_get_bottom_border(visual_board):
    visual_board.get_tile_size = lambda: 50
    assert visual_board.get_bottom_border() == 250


def test_is_position_in_board(visual_board):
    assert visual_board.is_position_in_board((50, 50)) is True
    assert visual_board.is_position_in_board((250, 250)) is True
    assert visual_board.is_position_in_board((0, 0)) is True
    assert visual_board.is_position_in_board((300, 300)) is False


def test_get_row_col_by_mouse(visual_board):
    assert visual_board.get_row_col_by_mouse((50, 50)) == (1, 1)
    assert visual_board.get_row_col_by_mouse((0, 0)) == (0, 0)
    assert visual_board.get_row_col_by_mouse((100, 100)) == (2, 2)


def test_place_ship(visual_board):
    ship = VisualShip(2, row=1, col=1, is_horizontal=True, coordinate_size=50, x=50, y=50)
    visual_board.place_ship(ship)
    assert ship.row == 1
    assert ship.col == 1
    assert ship.x == 50
    assert ship.y == 50


def test_reveal_ship_success(visual_board_enemy_view):
    ship = VisualShip(ship_length=2, row=1, col=1, is_horizontal=True, coordinate_size=VisualTile.TILE_SIZE)
    print(visual_board_enemy_view)

    result = visual_board_enemy_view.reveal_ship(ship, reveal_adjacent=True)
    print(visual_board_enemy_view)

    assert visual_board_enemy_view.shot_coordinates[(0, 0)] == 1
    assert visual_board_enemy_view.shot_coordinates[(0, 1)] == 1

    assert visual_board_enemy_view.shot_coordinates[(1, 0)] == 1
    assert visual_board_enemy_view.shot_coordinates[(1, 1)] == 1
    assert visual_board_enemy_view.shot_coordinates[(1, 2)] == 1
    assert visual_board_enemy_view.shot_coordinates[(1, 3)] == 1

    assert visual_board_enemy_view.shot_coordinates[(2, 1)] == 1
    assert visual_board_enemy_view.shot_coordinates[(2, 2)] == 1

    assert result is True


def test_reveal_ship_invalid_placement(visual_board_enemy_view):
    ship = VisualShip(ship_length=2, row=1, col=1, is_horizontal=True, coordinate_size=VisualTile.TILE_SIZE)

    with patch.object(visual_board_enemy_view, "is_ship_placement_valid", return_value=False):
        result = visual_board_enemy_view.reveal_ship(ship, reveal_adjacent=True)

        assert visual_board_enemy_view.shot_coordinates[(0, 0)] == 0
        assert visual_board_enemy_view.shot_coordinates[(0, 1)] == 0

        assert visual_board_enemy_view.shot_coordinates[(1, 0)] == 0
        assert visual_board_enemy_view.shot_coordinates[(1, 1)] == 0
        assert visual_board_enemy_view.shot_coordinates[(1, 2)] == 0
        assert visual_board_enemy_view.shot_coordinates[(1, 3)] == 0

        assert visual_board_enemy_view.shot_coordinates[(2, 1)] == 0
        assert visual_board_enemy_view.shot_coordinates[(2, 2)] == 0
        assert result is False


def test_set_hover_on_tile():
    tile = VisualTile(x=0, y=0)
    tile.set_hover(True)
    assert tile.is_hovered is True
    tile.set_hover(False)
    assert tile.is_hovered is False
