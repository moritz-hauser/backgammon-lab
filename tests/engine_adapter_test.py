import pytest
from unittest.mock import MagicMock

from bg_game.engine_adapter import EngineAdapter
from bg_game.game_types import (
    WHITE, BLACK, Color,
    NUM_POINTS,
    Move, Action, Dice,
    Point, Points,
    WorldState,
    OFF, BAR
)

def _emtpy_fv():
    """
    Returns an empty feature vector, as 
    used by the engine to represent the board. 
    """
    SZ_UNIT = 4
    # bar/off for BLACK/WHITE and [0.0, 1.1] for current player
    SZ_EXTRA_FIELDS = 6
    return [0.0] * (NUM_POINTS * SZ_UNIT * 2 + SZ_EXTRA_FIELDS)

def test_get_actions_can_handle_off_white():
    ad = EngineAdapter()
    ad.engine = MagicMock()
    ad.engine.get_valid_plays.return_value = {((3, -1),)}
    any_dice: Dice = (4, 5)

    expected: list[Action] = [((3, OFF),)]

    actual = ad.get_actions(WHITE, any_dice)

    assert expected == actual

def test_get_actions_can_handle_off_black():
    ad = EngineAdapter()
    ad.engine = MagicMock()
    ad.engine.get_valid_plays.return_value = {((20, 24),)}
    any_dice: Dice = (4, 5)

    expected: list[Action] = [((20, OFF),)]

    actual = ad.get_actions(BLACK, any_dice)

    assert expected == actual

def test_get_actions_can_handle_bar_white():
    ad = EngineAdapter()
    ad.engine = MagicMock()
    ad.engine.get_valid_plays.return_value = {(("bar", 23),)}
    any_dice: Dice = (1, 5)

    expected: list[Action] = [((BAR, 23),)]

    actual = ad.get_actions(WHITE, any_dice)

    assert expected == actual

def test_get_actions_can_handle_bar_black():
    ad = EngineAdapter()
    ad.engine = MagicMock()
    ad.engine.get_valid_plays.return_value = {(("bar", 0),)}
    any_dice: Dice = (1, 5)

    expected: list[Action] = [((BAR, 0),)]

    actual = ad.get_actions(BLACK, any_dice)

    assert expected == actual




def test_get_actions_black_passes_dice_unchanged():
    ad = EngineAdapter()
    ad.engine = MagicMock()
    any_action: Action = ((0,1),)
    ad.engine.get_valid_plays.return_value = {any_action}
    dice: Dice = (3, 5)
    actions: list[Action] = ad.get_actions(BLACK, dice)

    ad.engine.get_valid_plays.assert_called_once_with(BLACK, dice)
    # Set because we dont care about the order of the actions
    assert set(actions) == {((0, 1),)}

def test_get_actions_white_flips_dice_sign():
    ad = EngineAdapter()
    ad.engine = MagicMock()
    expected: list[Action] = [((0,1), (1,2),)]
    ad.engine.get_valid_plays.return_value = set(expected)

    dice: Dice = (2, 6)
    actual: list[Action] = ad.get_actions(WHITE, dice)

    ad.engine.get_valid_plays.assert_called_once_with(WHITE, (-2, -6))
    assert set(actual) == set(expected)

def test_get_actions_rejects_non_positive_dice():
    ad = EngineAdapter()
    ad.engine = MagicMock()

    with pytest.raises(AssertionError):
        ad.get_actions(WHITE, (0, 3))
    with pytest.raises(AssertionError):
        ad.get_actions(BLACK, (-1, 4))

def test_step_calls_execute_play():
    ad = EngineAdapter()
    ad.engine = MagicMock()

    ad.engine.get_board_features.return_value = _empty_fv()

    action: Action = ((0, 1), (1, 2))
    ad.step(WHITE, action)

    ad.engine.execute_play.assert_called_once_with(WHITE, action)
def _empty_fv():
    SZ_UNIT = 4
    SZ_BOARD_REP = NUM_POINTS * SZ_UNIT
    # [white features] + [bar_w, off_w] + [black features] + [bar_b, off_b] + [player_is_white, player_is_black]
    return [0.0]*(SZ_BOARD_REP) + [0.0, 0.0] + [0.0]*(SZ_BOARD_REP) + [0.0, 0.0] + [0.0, 0.0]

def test_get_state_calls_engine_and_converts():
    ad = EngineAdapter()
    ad.engine = MagicMock()

    fake_fv = _emtpy_fv()
    ad.engine.get_board_features.return_value = fake_fv

    ws: WorldState = ad.get_state()

    ad.engine.get_board_features.assert_called_once_with(WHITE)
    assert isinstance(ws, WorldState)
    assert len(ws.points) == NUM_POINTS 

