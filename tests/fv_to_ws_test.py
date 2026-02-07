import pytest
from unittest.mock import MagicMock

from bg_game.engine_adapter import EngineAdapter
from bg_game.game_types import (
    WHITE, BLACK, Color,
    NUM_POINTS,
    Move, Action, Dice,
    Point, Points,
    WorldState,
)

SZ_UNIT = 4
SZ_BOARD_REP = NUM_POINTS * SZ_UNIT

def _empty_fv():
    # [white features] + [bar_w, off_w] + [black features] + [bar_b, off_b] + [player_is_white, player_is_black]
    return [0.0]*(SZ_BOARD_REP) + [0.0, 0.0] + [0.0]*(SZ_BOARD_REP) + [0.0, 0.0] + [0.0, 0.0]

def _set_white_point(fv, target_field, unit):
    start = target_field * SZ_UNIT
    fv[start:start + SZ_UNIT] = unit

def _set_black_point(fv, target_field, unit):
    start = SZ_BOARD_REP + 2 + target_field*SZ_UNIT
    fv[start:start+SZ_UNIT] = unit

def test_fv_to_ws_empty_board():
    fv = _empty_fv()
    ws = EngineAdapter._feature_vector_to_world_state(fv)

    assert ws.bar == (0, 0)
    assert ws.off == (0, 0)
    assert all(p == (0, None) for p in ws.points)

def test_fv_to_ws_white_1_2_3_checkers():
    fv = _empty_fv()

    _set_white_point(fv, 0, [1.0, 0.0, 0.0, 0.0])  # 1
    _set_white_point(fv, 1, [1.0, 1.0, 0.0, 0.0])  # 2 (unit[1]!=0)
    _set_white_point(fv, 2, [1.0, 1.0, 1.0, 0.0])  # 3 (unit[2]!=0)

    ws = EngineAdapter._feature_vector_to_world_state(fv)

    assert ws.points[0] == (1, WHITE)
    assert ws.points[1] == (2, WHITE)
    assert ws.points[2] == (3, WHITE)

def test_fv_to_ws_black_1_2_3_checkers():
    fv = _empty_fv()

    _set_black_point(fv, 0, [1.0, 0.0, 0.0, 0.0])  # 1
    _set_black_point(fv, 1, [1.0, 1.0, 0.0, 0.0])  # 2
    _set_black_point(fv, 2, [1.0, 1.0, 1.0, 0.0])  # 3

    ws = EngineAdapter._feature_vector_to_world_state(fv)

    assert ws.points[0] == (1, BLACK)
    assert ws.points[1] == (2, BLACK)
    assert ws.points[2] == (3, BLACK)

def test_fv_to_ws_white_4_checkers():
    fv = _empty_fv()
    _set_white_point(fv, 10, [1.0, 1.0, 1.0, 0.5])  # 4 checkers

    ws = EngineAdapter._feature_vector_to_world_state(fv)
    assert ws.points[10] == (4, WHITE)

def test_fv_to_ws_black_4_checkers():
    fv = _empty_fv()
    _set_black_point(fv, 10, [1.0, 1.0, 1.0, 0.5])  # 4 checkers

    ws = EngineAdapter._feature_vector_to_world_state(fv)
    assert ws.points[10] == (4, BLACK)

def test_fv_to_ws_white_5_checkers():
    fv = _empty_fv()
    _set_white_point(fv, 23, [1.0, 1.0, 1.0, 1.0])  # 5 checkers

    ws = EngineAdapter._feature_vector_to_world_state(fv)
    assert ws.points[23] == (5, WHITE)

def test_fv_to_ws_black_5_checkers():
    fv = _empty_fv()
    _set_black_point(fv, 23, [1.0, 1.0, 1.0, 1.0])  # 5 checkers

    ws = EngineAdapter._feature_vector_to_world_state(fv)
    assert ws.points[23] == (5, BLACK)

def test_fv_to_ws_bar_off_scaling():
    fv = _empty_fv()

    expected_bar = (1, 2)
    bw, bb = expected_bar
    fv[SZ_BOARD_REP] = bw / 2   # bar is encoded as half
    fv[2*SZ_BOARD_REP + 2] = bb / 2
    
    expected_off = (3, 6)
    ow, ob = expected_off
    fv[SZ_BOARD_REP + 1] = ow / 15  # off is encoded as 1/15th
    fv[2*SZ_BOARD_REP + 3] = ob / 15    

    ws = EngineAdapter._feature_vector_to_world_state(fv)
    assert ws.bar == (1, 2)
    assert ws.off == (3, 6)


