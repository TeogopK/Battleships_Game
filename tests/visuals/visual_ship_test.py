import pytest
from game.visuals.visual_ship import VisualShip


@pytest.fixture
def visual_ship_1():
    return VisualShip(
        ship_length=1,
        row=1,
        col=1,
        is_horizontal=True,
        is_alive=True,
        sunk_coordinates=[(1, 1)],
        coordinate_size=20,
        x=100,
        y=150,
    )


@pytest.fixture
def visual_ship_2():
    return VisualShip(
        ship_length=2,
        row=1,
        col=1,
        is_horizontal=True,
        is_alive=True,
        sunk_coordinates=[(1, 1)],
        coordinate_size=20,
        x=100,
        y=150,
    )


@pytest.fixture
def visual_ship_2_vertical():
    return VisualShip(
        ship_length=2,
        row=1,
        col=1,
        is_horizontal=False,
        is_alive=True,
        sunk_coordinates=[(1, 1)],
        coordinate_size=20,
        x=100,
        y=150,
    )


def test_get_visual_length_horizontal_1(visual_ship_1):
    assert visual_ship_1.get_visual_length() == 20


def test_get_visual_width_horizontal_1(visual_ship_1):
    assert visual_ship_1.get_visual_width() == 20


def test_get_right_border_1(visual_ship_1):
    assert visual_ship_1.get_right_border() == 120


def test_get_bottom_border_1(visual_ship_1):
    assert visual_ship_1.get_bottom_border() == 170


def test_get_visual_length_horizontal_2(visual_ship_2):
    assert visual_ship_2.get_visual_length() == 40


def test_get_visual_width_horizontal_2(visual_ship_2):
    assert visual_ship_2.get_visual_width() == 20


def test_get_right_border_2(visual_ship_2):
    assert visual_ship_2.get_right_border() == 140


def test_get_bottom_border_2(visual_ship_2):
    assert visual_ship_2.get_bottom_border() == 170


def test_get_visual_length_vertical_2(visual_ship_2_vertical):
    assert visual_ship_2_vertical.get_visual_length() == 20


def test_get_visual_width_vertical_2(visual_ship_2_vertical):
    assert visual_ship_2_vertical.get_visual_width() == 40


def test_get_right_border_vertical_2(visual_ship_2_vertical):
    assert visual_ship_2_vertical.get_right_border() == 120


def test_get_bottom_border_vertical_2(visual_ship_2_vertical):
    assert visual_ship_2_vertical.get_bottom_border() == 190


def test_update_visual_position_1(visual_ship_1):
    visual_ship_1.update_visual_position(200, 250)
    assert visual_ship_1.x == 200
    assert visual_ship_1.y == 250


def test_update_visual_position_2(visual_ship_2):
    visual_ship_2.update_visual_position(200, 250)
    assert visual_ship_2.x == 200
    assert visual_ship_2.y == 250


def test_set_color_1(visual_ship_1):
    new_color = (255, 0, 0)
    visual_ship_1.set_color(new_color)
    assert visual_ship_1.color == new_color


def test_set_color_2(visual_ship_2):
    new_color = (0, 255, 0)
    visual_ship_2.set_color(new_color)
    assert visual_ship_2.color == new_color
