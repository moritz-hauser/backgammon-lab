from bg_game.game_types import AgentPerspectiveState, NUM_POINTS, WorldState, Points, NUM_CHECKERS_EACH, WHITE, BLACK, Point
import pytest

def test_valid_state_construction_successful():
    points_list = [0] * NUM_POINTS
    points_list[23] = 1
    points_list[5] = -6
    points_list[10] = -6
    points_list[4] = -2

    aps = AgentPerspectiveState(
        points=tuple(points_list),
        bar_me=2,
        bar_enemy=0,
        off_me=12,
        off_enemy=1
    )

def test_invalid_state_construction_fail():
    points_list = [0] * NUM_POINTS
    points_list[23] = 1
    points_list[5] = -6
    points_list[10] = -6
    points_list[4] = -2 + 1 # to few enemy checkers
    
    with pytest.raises(AssertionError):
        AgentPerspectiveState(
            points=tuple(points_list),
            bar_me=2,
            bar_enemy=0,
            off_me=12,
            off_enemy=1
        )

def _valid_ws() -> WorldState:
    """
    12 WHITE @ 23
    13 BLACK @ 0
    03 WHITE @ off
    01 BLACK @ off
    00 WHITE @ bar
    01 BLACK @ bar
    """
    empty_points: list[Point] = [(0, None)] * NUM_POINTS
    empty_points[23] = (NUM_CHECKERS_EACH-3, WHITE)
    empty_points[0] = (NUM_CHECKERS_EACH-2, BLACK)

    return WorldState(
        points = tuple(empty_points),
        off = (3, 1),
        bar = (0, 1)
    )
    

def test_from_valid_ws_white_flips_board():
    aps = AgentPerspectiveState.from_world_state(_valid_ws(), WHITE)

    assert aps.bar_me == 0
    assert aps.bar_enemy == 1
    assert aps.off_me == 3
    assert aps.off_enemy == 1

    assert aps.points[0] == 12
    assert aps.points[23] == -13

def test_from_valid_ws_black_converts_correctly():
    aps = AgentPerspectiveState.from_world_state(_valid_ws(), BLACK)

    assert aps.bar_me == 1
    assert aps.bar_enemy == 0
    assert aps.off_me == 1
    assert aps.off_enemy == 3

    assert aps.points[0] == 13
    assert aps.points[23] == -12
