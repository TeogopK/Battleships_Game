import pytest
from unittest.mock import Mock, patch
from game.players.battle_bot import BattleBot


@pytest.fixture
def bot():
    network_client_mock = Mock()
    bot_instance = BattleBot(network_client_mock)
    bot_instance.board = Mock()
    bot_instance.enemy_board_view = Mock()
    bot_instance.enemy_board_view.is_coordinate_shot_at.return_value = False
    return bot_instance, network_client_mock


def test_initial_state(bot):
    bot_instance, _ = bot
    assert bot_instance.shot_history == set()
    assert bot_instance.hit_stack == []
    assert bot_instance.hunting_mode is False
    assert bot_instance.last_hit is None
    assert bot_instance.is_horizontal is None
    assert not bot_instance.is_in_finished_battle


def test_reset_hunting_strategy(bot):
    bot_instance, _ = bot

    bot_instance.hunting_mode = True
    bot_instance.shot_history.add((1, 1))
    bot_instance.hit_stack.append((2, 2))
    bot_instance.last_hit = (2, 2)
    bot_instance.is_horizontal = True

    bot_instance._reset_hunting_strategy()

    assert bot_instance.hunting_mode is False
    assert bot_instance.shot_history == set()
    assert bot_instance.hit_stack == []
    assert bot_instance.last_hit is None
    assert bot_instance.is_horizontal is None


def test_stop_bot(bot):
    bot_instance, _ = bot
    bot_instance.stop_bot()
    assert bot_instance.is_in_finished_battle is True


def test_perform_attack_random(bot):
    bot_instance, _ = bot

    bot_instance._select_random_position = Mock(return_value=(2, 3))
    bot_instance.shot = Mock(return_value={"status": "success", "args": {"has_hit_ship": False}})
    bot_instance._process_attack_result = Mock()

    bot_instance.perform_attack()

    bot_instance._select_random_position.assert_called_once()
    bot_instance.shot.assert_called_once_with(2, 3)
    bot_instance._process_attack_result.assert_called_once_with({"status": "success", "args": {"has_hit_ship": False}}, 2, 3)


def test_perform_attack_in_finished_battle(bot):
    bot_instance, _ = bot
    bot_instance.is_in_finished_battle = True
    bot_instance.perform_attack()
    assert not bot_instance.is_turn


def test_get_attack_position_random(bot):
    bot_instance, _ = bot

    bot_instance.hunting_mode = False
    bot_instance._select_random_position = Mock(return_value=(5, 5))

    position = bot_instance._get_attack_position()

    assert position == (5, 5)
    bot_instance._select_random_position.assert_called_once()


def test_get_attack_position_hunting(bot):
    bot_instance, _ = bot

    bot_instance.hunting_mode = True
    bot_instance.hit_stack = [(2, 3)]

    position = bot_instance._get_attack_position()

    assert position == (2, 3)
    assert bot_instance.hit_stack == []


def test_select_random_position(bot):
    bot_instance, _ = bot
    bot_instance.board.rows_count = 10
    bot_instance.board.columns_count = 10

    bot_instance.shot_history = {(2, 3), (4, 5)}

    with patch("random.randint", side_effect=[7, 8]):
        random_position = bot_instance._select_random_position()

    assert random_position == (7, 8)
    assert (7, 8) not in bot_instance.shot_history


def test_process_attack_result_hit(bot):
    bot_instance, _ = bot

    bot_instance._update_hunting_strategy = Mock()
    bot_instance._reset_hunting_strategy = Mock()

    # Test when ship is hit but not sunk
    bot_instance._process_attack_result({"status": "success", "args": {"has_hit_ship": True, "has_sunk_ship": False}}, 2, 3)
    bot_instance._update_hunting_strategy.assert_called_once_with(2, 3)
    bot_instance._reset_hunting_strategy.assert_not_called()
    assert bot_instance.hunting_mode is True

    # Test when ship is hit and sunk
    bot_instance._process_attack_result({"status": "success", "args": {"has_hit_ship": True, "has_sunk_ship": True}}, 2, 3)
    bot_instance._reset_hunting_strategy.assert_called_once()


def test_process_attack_result_miss(bot):
    bot_instance, _ = bot
    bot_instance._update_hunting_strategy = Mock()
    bot_instance._reset_hunting_strategy = Mock()

    bot_instance._process_attack_result({"status": "success", "args": {"has_hit_ship": False, "has_sunk_ship": False}}, 2, 3)

    bot_instance._update_hunting_strategy.assert_not_called()
    bot_instance._reset_hunting_strategy.assert_not_called()
    assert bot_instance.hunting_mode is False


def test_update_hunting_strategy(bot):
    bot_instance, _ = bot

    bot_instance.last_hit = (2, 3)
    bot_instance._set_direction = Mock()
    bot_instance._generate_line_positions = Mock(return_value=[(2, 4), (2, 2)])
    bot_instance._add_positions_to_stack = Mock()

    bot_instance._update_hunting_strategy(2, 4)

    bot_instance._set_direction.assert_called_once_with(2)
    bot_instance._generate_line_positions.assert_called_once_with(2, 4)
    bot_instance._add_positions_to_stack.assert_called_once_with([(2, 4), (2, 2)])
    assert bot_instance.last_hit == (2, 4)


def test_set_direction(bot):
    bot_instance, _ = bot

    bot_instance.last_hit = (2, 3)

    bot_instance._set_direction(2)
    assert bot_instance.is_horizontal is True

    bot_instance._set_direction(1)
    assert bot_instance.is_horizontal is False


def test_generate_adjacent_positions():
    positions = BattleBot._generate_adjacent_positions(5, 5)
    expected_positions = [(4, 5), (6, 5), (5, 4), (5, 6)]
    assert positions == expected_positions


def test_generate_line_positions_horizontal(bot):
    bot_instance, _ = bot
    bot_instance.is_horizontal = True

    positions = bot_instance._generate_line_positions(5, 5)
    expected_positions = [(5, 4), (5, 6)]

    assert positions == expected_positions


def test_generate_line_positions_vertical(bot):
    bot_instance, _ = bot
    bot_instance.is_horizontal = False

    positions = bot_instance._generate_line_positions(5, 5)
    expected_positions = [(4, 5), (6, 5)]

    assert positions == expected_positions


def test_add_positions_to_stack(bot):
    bot_instance, _ = bot

    bot_instance.shot_history = {(2, 3)}
    bot_instance.board.is_coordinate_in_board = Mock(return_value=True)

    bot_instance._add_positions_to_stack([(2, 3), (3, 4)])

    assert bot_instance.hit_stack == [(3, 4)]
